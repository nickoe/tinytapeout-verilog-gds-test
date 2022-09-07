#!/usr/bin/env python3
import logging
import datetime
import time


from amaranth.compat import *
from litex.soc.cores.led import LedChaser
from litex.build.generic_platform import *
from litex.soc.integration.builder import *
from litex.build.sim import SimPlatform
from litex.build.sim.config import SimConfig

logging.basicConfig(level=logging.INFO)

def colorer(s, color="bright"):
    header  = {
        "bright": "\x1b[1m",
        "green":  "\x1b[32m",
        "cyan":   "\x1b[36m",
        "red":    "\x1b[31m",
        "yellow": "\x1b[33m",
        "underline": "\x1b[4m"}[color]
    trailer = "\x1b[0m"
    return header + str(s) + trailer

def build_time(with_time=True):
    fmt = "%Y-%m-%d %H:%M:%S" if with_time else "%Y-%m-%d"
    return datetime.datetime.fromtimestamp(time.time()).strftime(fmt)

_io = [
    ("sys_clk", 0, Pins(1)),
    ("sys_rst", 0, Pins(1)),
    ("user_led", 0, Pins(1)),
    ("user_led", 1, Pins(1)),
    ("user_led", 2, Pins(1)),
    ("user_led", 3, Pins(1)),
]


#class TinyTapeoutPlatform(GenericPlatform):
class TinyTapeoutPlatform(SimPlatform):
    def __init__(self):
        SimPlatform.__init__(self, device="SIM", io=_io)


class MyModule(Module):
    def __init__(self, platform, sys_clk_freq):
        self.logger = logging.getLogger("NICK DEBUG MyModule")
        self.logger.info(colorer("Creating SoC... ({})".format(build_time())))
        self.logger.info("FPGA device : {}.".format(platform.device))
        self.logger.info("System clock: {:3.3f}MHz.".format(sys_clk_freq/1e6))

        # SoC attributes ---------------------------------------------------------------------------
        self.platform     = platform
        self.sys_clk_freq = sys_clk_freq
        self.constants    = {}
        self.csr_regions  = {}

        # CRG --------------------------------------------------------------------------------------
        #self.submodules.crg = CRG(platform.request("sys_clk"))

        # Leds -------------------------------------------------------------------------------------
        self.submodules.leds = LedChaser(
            pads         = platform.request_all("user_led"),
            sys_clk_freq = sys_clk_freq)
        #self.add_csr("leds")


def main():
    sys_clk_freq = int(1e6)
    sim_config = SimConfig()
    sim_config.add_clocker("sys_clk", freq_hz=sys_clk_freq)

    platform = TinyTapeoutPlatform()
    sim = MyModule(platform, sys_clk_freq)

    # builder = Builder(my_mod)
    # builder.build(
    #     compile_software = False,
    #     compile_gateware = True,
    #     sim_config       = sim_config,
    #     trace            = True,
    #     trace_fst        = True,
    #     trace_start      = 0,
    #     trace_end        = 1000,
    # )
    platform.build(sim, build_dir="./", run=False )
    pass


if __name__ == "__main__":
    main()

