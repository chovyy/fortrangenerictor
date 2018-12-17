SB2_ROOT = ../serialbox2
SB2_SRC = $(SB2_ROOT)/src/serialbox-fortran
SB2_BUILD = $(SB2_ROOT)/build

test: build
	$(SB2_ROOT)/build/install/run_tests.sh

build: $(SB2_SRC)/m_ser_ftg.f90 $(SB2_SRC)/m_ser_ftg_cmp.f90
	$(MAKE) -C $(SB2_BUILD)
	
$(SB2_SRC)/m_ser_ftg.f90: m_ser_ftg.f90.cht
	printf '\e[38;5;0m\e[48;5;104mm_ser_ftg.f90.cht > $(SB2_SRC)/m_ser_ftg.f90\e[48;5;0m\n\e[38;5;15m'
	./FortranGenerictor.py m_ser_ftg.f90.cht > $(SB2_SRC)/m_ser_ftg.f90
	
$(SB2_SRC)/m_ser_ftg_cmp.f90: m_ser_ftg_cmp.f90.cht
	printf '\e[38;5;0m\e[48;5;104mm_ser_ftg_cmp.f90.cht > $(SB2_SRC)/m_ser_ftg_cmp.f90\e[48;5;0m\n\e[38;5;15m'
	./FortranGenerictor.py m_ser_ftg_cmp.f90.cht > $(SB2_SRC)/m_ser_ftg_cmp.f90
	
.PHONY: test build