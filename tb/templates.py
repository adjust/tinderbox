EMERGE = """
emerge \
--autounmask \
--autounmask-write=n \
--buildpkg=y \
--buildpkg-exclude="{bin_exclude}" \
--changed-deps=y \
--color=y \
--complete-graph=y \
--config-root="{config_root}" \
--deep \
--exclude="{exclude}" \
--getbinpkg=n \
--getbinpkgonly=n \
--jobs="{jobs}" \
--load-average="{jobs}" \
--misspell-suggestions=n \
--newuse \
--root="{root}" \
--update \
--with-bdeps=y \
""".strip()


CREATE_TARGETS = """
trex -t max -E nosudo -G all Adjust:Binhost:create_target --root={root}
""".strip()


UPDATE_SINGLE_TARGET = """
trex -E nosudo -H {target} Adjust:Binhost:genpcfg --root={root}
""".strip()
