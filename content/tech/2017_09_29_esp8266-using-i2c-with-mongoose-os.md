Title: ESP8266: Using I2C with Mongoose OS
Date: 2017-9-29 9:42
Tags: esp8266, mongoose os, mcp23017, i2c
Category: Tech
Slug: esp8266-using-i2c-with-mongoose-os
Summary: I2C with a MCP23017 GPIO Expansion IC and an ESP8266 with Mongoose
Status: published

A project I'm working on recently required more GPIO pins than the ESP8266 I'm working with had
available. That lead me to select a 
[Microchip MCP23017 I2C GPIO expander](http://www.microchip.com/wwwproducts/en/MCP23017) to expand
the available GPIO. I'm using [Mongoose OS](http://www.mongoose-os.com) for this particular project
so I needed to figure out how to get the I2C interface to work.

I'm relatively new to both Mongoose and the ESP8266 but so far I really like them both. That said, I
had trouble finding a good source of information for Mongoose and I2C. It took me piecing things
together from various places and some good ol' experimentation to figure it out. It ended up being
far easier than I thought once I got all the pieces lined up so I'm documenting it here so that it's
a resource for myself and anyone else who has the same problems or questions I did.

First up, the app needs to have I2C enabled and the relevant library added. This is accomplished via
mos.yml, the primary YAML configuration file in the app's root directory. To start with, enable I2C
in the config section:

```yaml
# mos.yml

config_schema:
  - ["i2c.enable", true]

# Some googling might turn up references like these in this file:
# - ["i2c.sda_pin", 2]
# - ["i2c.scl_pin", 0]
# Don't use them. This is for an older version of Mongoose.
```

Next add the library at the bottom of the file:

```yaml
# mos.yml

# There will likely be a number of other libs here. I just added this line to the bottom.
libs:
  - origin: https://github.com/mongoose-os-libs/i2c
```

Here's the part that stumped me for a while, especially when I saw bits of information scattered
around the Interwebs about declaring which GPIO pins to use for SDA and SCL as part of config_schema
section of mos.yml as described in code comments above. I had a hard time finding information on
exactly what Mongoose does once I2C is enabled in the app config file. What pins were used for for
the bus lines by default? I finally found the answer by building the app and then poking around in
the app's 'build/fs' subdirectory. Specifically, the conf0.json file gets the following section added
to it automagically when i2c.enable is set to True in mos.yml:

```json
{
    "i2c": {
        "enable": true, 
        "freq": 100000, 
        "debug": false, 
        "sda_gpio": 12, 
        "scl_gpio": 14
    }
}
```

And there we go. GPIO pins 12 and 14 (or D6 and D5, if you're using a NodeMCU development board as
I was) are the default I2C bus pins. From this point it gets even easier, though the Mongoose
documentation is a little light on the subject and the [examples I found](https://github.com/cesanta/mongoose-os/blob/master/fw/examples/c_mqtt/src/main.c) weren't great. Don't let that scare you though, it's not bad at all. Looking at the
[documentation for the I2C api](https://mongoose-os.com/docs/libraries/hardware/i2c.html) and
focusing on the C portion of it, we see that all the functions require a pointer to a mgos_i2c
structure as the first parameter. This is easily obtained by reading the configuration:

```c
// Be sure to include mgos_sys_config.h
struct mgos_i2c *i2c = mgos_i2c_get_global();
```

Then, for the sake of simplicity, we'll stick to the register byte read and write functions. The
word functions work the same way but read/write two bytes instead of one. This could be useful if,
for example, you're dealing with the to GPIO banks as one big (16 bit) register instead of two
separate (8 bit) ones.  Be sure to read the docs for specifics on things like byte order. Anyway,
to write a byte to GPIO Bank A all we have to do is this:

```c
bool ret = mgos_i2c_write_reg_b(i2c, 0x20, 0x12, 0xff);
```

The write operation takes four parameters:

* A pointer to an mgos_i2c struct as obtained above
* The I2C bus address of the device we're trying to talk to. In this case the MCP23017 has all
  three address pins wired to ground, giving it a default address of 0x20 (or integer 32).
* The address of the device register we want to write to. 0x12 is the default address of the
  MCP23017's GPIOA register, which is the eight "Bank A" GPIO pins.
* The value to write to the register addressed in the previous parameter. Here we're just setting
  all bits in the GPIO bank to 1.

The return value of the function is a boolean indicating success or failure of the write operation.

Reading from the device is just as easy:

```c
int ret = mgos_i2c_write_reg_b(i2c, 0x20, 0x12);
```

The read operation only needs three parameters. They are exactly the same as the write with the
obvious exception that we don't need the fourth "value to write" parameter. The return value is an
integer reflecting the state of the register's pins. If all eight are high, we'd get 0xff as a
return value.

In the interests of being thorough and making sure evering is clear, here's the full code for minimal
example program. This program uses a ESP8266 and a MCP2017, an LED, a resistor, a momentary switch,
and whatever wire is required.

* Wire one side of the button to ground, the other side to GPIO4 of the ESP8266. We're using an
  internal pull-up resistor so that's all that's needed for the button.
* Wire all three address pins of the MCP23017 to ground for a default address of 0x20. Otherwise
  change the second parameter of all the I2C read/write functions to match whatever address the
  23017 is configured for.
* Wire the anode of an LED to one of the 23017's Bank A GPIO pins. Wire the cathode to ground
  through a current-limiting resistor. 

Example schematic:  
![Example Schematic]({attach}../images/ESP_MCP_I2C_Schematic.png)  

Code:

```c
#include "mgos.h"
#include "mgos_gpio.h"
#include "mgos_sys_config.h"
#include "mgos_i2c.h"

static volatile bool led_state = false;

static void expansion_io_setup() {
    struct mgos_i2c *i2c = mgos_i2c_get_global();
    if(i2c == NULL) {
        LOG(LL_INFO, ("I2C is not enabled!"));
    }
    else {
        // Make sure IOCON.BANK = 0
        mgos_i2c_write_reg_b(i2c, 0x20, 0x0a, 0x00);
        // Set all the pins in GPIO Bank A as outputs
        mgos_i2c_write_reg_b(i2c, 0x20, 0x00, 0x00);
    }
}

static void i2c_write() {
    struct mgos_i2c *i2c = mgos_i2c_get_global();
    if(i2c == NULL) {
        LOG(LL_INFO, ("I2C is not enabled!"));
    }
    else {
        bool ret;
        if(led_state)
            ret = mgos_i2c_write_reg_b(i2c, 0x20, 0x12, 0x00);
        else
            ret = mgos_i2c_write_reg_b(i2c, 0x20, 0x12, 0xff);

        if(ret)
            led_state = !led_state;

        LOG(LL_INFO, ("GPIOA Register write returned %i", ret));
    }
}

static void i2c_read() {
    struct mgos_i2c *i2c = mgos_i2c_get_global();
    if(i2c == NULL) {
        LOG(LL_INFO, ("I2C is not enabled!"));
    }
    else {
        int ret;
        ret = mgos_i2c_read_reg_b(i2c, 0x20, 0x12);
        LOG(LL_INFO, ("GPIOA Register value is %i", ret));
    }
}

static void button_cb(int pin, void *arg) {
    i2c_write();
    i2c_read();
    (void) pin;
    (void) arg;
}

enum mgos_app_init_result mgos_app_init(void) {
    expansion_io_setup();

    // Set up GPIO4 as a button input, connect an LED between one
    // of the Bank A GPIO pins to ground through a current-limiting
    // resistor.
    mgos_gpio_set_mode(4, MGOS_GPIO_MODE_INPUT);
    mgos_gpio_set_button_handler(4, MGOS_GPIO_PULL_UP,
        MGOS_GPIO_INT_EDGE_POS, 250, button_cb, NULL);

    return MGOS_APP_INIT_SUCCESS;
}
```
When built, flashed, and run, this code will toggle the LED attached to the 23017 when the button
pressed. It's really that simple! I hope this helps someone get answers quickly. Happy tinkering!
