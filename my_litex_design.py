#!/usr/bin/env python3

import argparse
from litex.build.generic_platform import *
from litex.build.sim import SimPlatform
from litex.build.sim.config import SimConfig
from litex.build.sim.verilator import verilator_build_args, verilator_build_argdict
from litex.soc.cores.led import LedChaser
from litex.soc.integration.builder import *
# from amaranth.compat import *
from migen import *

from litex.soc.integration.soc_core import *
from litex.soc.integration.soc import *
from litex.soc.cores.cpu import CPUS

_io = [
    ("sys_clk", 0, Pins(1)),
    ("sys_rst", 0, Pins(1)),
    ("serial", 0,
     Subsignal("source_valid", Pins(1)),
     Subsignal("source_ready", Pins(1)),
     Subsignal("source_data", Pins(8)),

     Subsignal("sink_valid", Pins(1)),
     Subsignal("sink_ready", Pins(1)),
     Subsignal("sink_data", Pins(8)),
     ),
    ("io_in", 0, Pins(8)),
    ("io_out", 0, Pins(8)),
]

class MyPlatform(GenericPlatform):
    def __init__(self):
        GenericPlatform.__init__(self, device="tapeout", io=_io, name="user_module_342176160444056147")

class TinyTapeoutPlatform(SimPlatform):
    def __init__(self):
        SimPlatform.__init__(self, device="SIM", io=_io, name="sim")

class SimSoC(SoCMini):
    def __init__(self, **kwargs):
        sys_clk_freq = int(1e6)
        platform = TinyTapeoutPlatform()
        # SoCCore ----------------------------------------------------------------------------------
        SoCCore.__init__(self, platform, clk_freq=sys_clk_freq,
            ident         = "LiteX Simulation  ____",
            **kwargs)

        # CRG --------------------------------------------------------------------------------------
        #self.submodules.crg = CRG(platform.request("sys_clk"))

        # Simulation platform ----------------------------------------------------------------------
        # Only in SimPlatform, has to be enabled for tracing to run
        if platform.device == "SIM":
            self.comb += platform.trace.eq(1)

        self.submodules.mymod = MyModule(platform, sys_clk_freq)
        pass

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
            pass



def wokwi_module_name():
    with open("src/ID") as f:
        WOKWI_PROJECT_ID = f.readline().strip()
    return f"user_module_{WOKWI_PROJECT_ID}"


def sim_args(parser):
    builder_args(parser)
    soc_core_args(parser)
    verilator_build_args(parser)


def main():
    sys_clk_freq = int(1e6)

    # Verilog for tapeout ----------------------------------------------------------------------
    # non_sim_platform = MyPlatform()
    # non_sim_platform.name = wokwi_module_name()
    # my_mod = MyModule(non_sim_platform, sys_clk_freq)
    # v_output = non_sim_platform.get_verilog(fragment=my_mod, name=non_sim_platform.name)
    # v_output.write(f"src/{non_sim_platform.name}.v")





    # Configuration --------------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description="Generic LiteX SoC Simulation")
    sim_args(parser)
    args = parser.parse_args()

    soc_kwargs = soc_core_argdict(args)
    builder_kwargs = builder_argdict(args)
    verilator_build_kwargs = verilator_build_argdict(args)


    #cpu = CPUS.get(soc_kwargs.get("cpu_type", "vexriscv"))

    sim_config = SimConfig()
    sim_config.add_clocker("sys_clk", freq_hz=sys_clk_freq)
    # UART.
    if soc_kwargs["uart_name"] == "serial":
        soc_kwargs["uart_name"] = "sim"
        sim_config.add_module("serial2console", "serial")

    # SoC ------------------------------------------------------------------------------------------

    soc = SimSoC(
                 with_ethernet=False,
                 with_etherbone=False,
                 with_analyzer=False,
                 with_i2c=False,
                 with_sdcard=False,
                 with_spi_flash=False,
                 with_gpio=False,
                 sim_debug=False,
                 trace_reset_on=False,
                 **soc_kwargs
                 )

    builder = Builder(soc, **builder_kwargs)
    builder.build(
        sim_config       = sim_config,
        interactive=True,
        run=True,
        **verilator_build_kwargs,
    )



if __name__ == "__main__":
    main()
