#!/usr/bin/env python3
import logging
import datetime
import time


#from amaranth.compat import *
from migen import *

from litex.soc.cores.led import LedChaser
from litex.build.generic_platform import *
from litex.soc.integration.builder import *
from litex.build.sim import SimPlatform
from litex.build.sim.config import SimConfig

_io = [
    ("sys_clk", 0, Pins(1)),
    ("sys_rst", 0, Pins(1)),
    ("user_led", 0, Pins(1)),
    ("user_led", 1, Pins(1)),
    ("user_led", 2, Pins(1)),
    ("user_led", 3, Pins(1)),
    ("user_led", 4, Pins(1)),
    ("user_led", 5, Pins(1)),
    ("user_led", 6, Pins(1)),
]

class TinyTapeoutPlatform(SimPlatform):
    def __init__(self):
        SimPlatform.__init__(self, device="SIM", io=_io, name="user_module_342176160444056147")


class MyModule(Module):
    def __init__(self, platform, sys_clk_freq):
        print("NICK DEBUG MyModule")

        # SoC attributes ---------------------------------------------------------------------------
        self.platform     = platform
        self.sys_clk_freq = sys_clk_freq
        self.constants    = {}
        self.csr_regions  = {}

        # CRG --------------------------------------------------------------------------------------
        self.submodules.crg = CRG(clk=platform.request("sys_clk"), rst=platform.request("sys_rst"))

        # Leds -------------------------------------------------------------------------------------
        self.submodules.leds = LedChaser(
            pads         = platform.request_all("user_led"),
            sys_clk_freq = sys_clk_freq)
        #self.add_csr("leds")

        self.comb += platform.trace.eq(1)


def main():
    sys_clk_freq = int(1e6)
    sim_config = SimConfig()
    sim_config.add_clocker("sys_clk", freq_hz=sys_clk_freq)

    platform = TinyTapeoutPlatform()
    sim = MyModule(platform, sys_clk_freq)
    platform.build(sim, sim_config=sim_config, interactive=True, build_dir="./litex_out", run=True,
                   trace=True,
                   trace_fst=True,
                   trace_start=0,
                   trace_end=-1,
                   )
    print("exit")


if __name__ == "__main__":
    main()

