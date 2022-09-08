#!/usr/bin/env python3


from litex.build.generic_platform import *
from litex.build.sim import SimPlatform
from litex.build.sim.config import SimConfig
from litex.soc.cores.led import LedChaser
from litex.soc.integration.builder import *
# from amaranth.compat import *
from migen import *

_io = [
    ("sys_clk", 0, Pins(1)),
    ("sys_rst", 0, Pins(1)),
    ("io_in", 0, Pins(8)),
    ("io_out", 0, Pins(8)),
]

class MyPlatform(GenericPlatform):
    def __init__(self):
        GenericPlatform.__init__(self, device="tapeout", io=_io, name="user_module_342176160444056147")

class TinyTapeoutPlatform(SimPlatform):
    def __init__(self):
        SimPlatform.__init__(self, device="SIM", io=_io, name="sim")


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

        #platform.request("io_out", 0),

        platform.request_all("io_in")

        # new matching in newer litex?
        #platform.request_remaining("io_in")


        # Only in SimPlatform, has to be enabled for tracing to run
        if platform.device == "SIM":
            self.comb += platform.trace.eq(1)


def wokwi_module_name():
    with open("src/ID") as f:
        WOKWI_PROJECT_ID = f.readline().strip()
    return f"user_module_{WOKWI_PROJECT_ID}"


def main():
    sys_clk_freq = int(1e6)

    # Verilog for tapeout ----------------------------------------------------------------------
    non_sim_platform = MyPlatform()
    non_sim_platform.name = wokwi_module_name()
    my_mod = MyModule(non_sim_platform, sys_clk_freq)
    v_output = non_sim_platform.get_verilog(fragment=my_mod, name=non_sim_platform.name)
    v_output.write(f"src/{non_sim_platform.name}.v")
    exit(0)

    # Simulation platform ----------------------------------------------------------------------
    platform = TinyTapeoutPlatform()
    sim = MyModule(platform, sys_clk_freq)
    sim_config = SimConfig()
    sim_config.add_clocker("sys_clk", freq_hz=sys_clk_freq)
    platform.build(sim, sim_config=sim_config, interactive=True, build_dir="./litex_out", run=True,
                   trace=True,
                   trace_fst=True,
                   trace_start=0,
                   trace_end=-1,
                   )


if __name__ == "__main__":
    main()
