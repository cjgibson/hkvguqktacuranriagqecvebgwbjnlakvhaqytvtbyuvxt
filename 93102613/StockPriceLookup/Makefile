DAYS ?= 7
START ?= $(shell uname -o | grep -qi linux && date --date="${DAYS} days ago" +'%Y-%m-%d' || date "-v-${DAYS}d" +'%Y-%m-%d')

.PHONY: vars
vars:
	@echo " DAYS = '$(DAYS)'"
	@echo "START = '$(START)'"

.PHONY: generate
.DEFAULT_GOAL := generate
generate:
	@python3 ./stock_lookup.py \
		--include-dates \
		--start=${START} \
		--days=${DAYS} \
		VASGX \
		VGENX \
		VGSIX \
		VTIAX \
		MONEY=1 \
		VBMFX \
		VTSAX \
		FSTVX=NaN \
		VBTLX \
		XVZ=NaN \
		EFX \
		UVXY \
		MPXEF=NaN \
		V \
		VTEAX \
		FTIGX=NaN \
		VGSLX \
		FTIPX=NaN \
		VTABX \
		VGTSX \
		VFIAX \
		TSLA \
		AAPL \
		FEMKX \
		GOOG \
		MSFT \
		AMZN \
		WMT \
		FSKAX \
		ze.SFYD=0 \
		BRK.B \
		JPM \
		WY \
		VTI \
		VEA \
		VWO \
		VTV \
		VOE \
		VBR \
		AGG \
		BNDX \
		EMB \
		VTIP \
		VOO \
		VB \
		VNQ \
		SHY \
		LQD \
		FSRNX \
		FTIHX \
		FXNAX \
		EXIV=NaN \
		SVXY \
		SPXU \
		SHV \
		VXUS \
		BND \
		VTMGX \
		VBILX \
		ze.EVEN=7.52810468451243 \
		ze.OPEN=0 \
		DDOG \
		zc.GUSD=NaN \
		BLZE \
		zc.FIL=NaN \
		zb.SISB=1 \
		zb.52TB=1 \
		zb.26TB=1 \
		zb.04TB=1 \
		zb.17TB=1
