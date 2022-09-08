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
    ("io_in", 0, Pins(8)),
    ("io_out", 0, Pins(8)),
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
        ledchaser = LedChaser(
            pads         = platform.request_all("io_out"),
            sys_clk_freq = sys_clk_freq)
        self.submodules.leds = ledchaser
        # control of brightness...
        ledchaser.add_pwm(default_width=900)
        #self.add_csr("leds")

        #self.comb += ledchaser.mode.eq(1)

        self.comb += platform.trace.eq(1)

        platform.request_all("io_in"),


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

