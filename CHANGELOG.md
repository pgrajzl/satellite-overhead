# CHANGELOG



## v0.5.0 (2024-02-14)


### Feature

* feat: Add __str__ impl for Configuration, Reservation, FrequencyRange, Facility and TimeWindow classes. ([`e9806dc`](https://github.com/NSF-Swift/satellite-overhead/commit/e9806dc0a7699d904893db1a1fecf78432cdc73e))

* feat: set_time_window() now accepts datetimes as well as datetime strings. ([`5bf9196`](https://github.com/NSF-Swift/satellite-overhead/commit/5bf9196695d69db64c0b1716f01c9bd90e493e16))


### Fix

* fix: Resolve the requirement for an observation target to be set when building a configuration as an observation target is not necessary if checking for satellites above horizon. ([`b610c19`](https://github.com/NSF-Swift/satellite-overhead/commit/b610c197f0172f5c985c0180de303bd1bc796dea))


### Refactor

* refactor: When None is passed to any filtering function they now return a lambda that always evaluates to True instead of failing. ([`fda8d2f`](https://github.com/NSF-Swift/satellite-overhead/commit/fda8d2fd2103c4977db395e5180a1fa3917a3399))

* refactor: Extract bandwidth and frequency from set_facility and move to seperate method set_frequency_range. ([`8c51e69`](https://github.com/NSF-Swift/satellite-overhead/commit/8c51e699fb15aef547e69143b45fdaaf36cf2fd2))

* refactor: Use a single orbit_is function instead of a seperate function for leo/meo/geo. ([`9c57292`](https://github.com/NSF-Swift/satellite-overhead/commit/9c57292c37934af5b34f4a9218798440767bd0af))



## v0.4.0 (2024-01-25)



## v0.3.1 (2024-01-24)


### Build

* build: Bump Skyfield dependency from 1.45 to 1.47. ([`55e4df0`](https://github.com/NSF-Swift/satellite-overhead/commit/55e4df0776f9660342ad281d8d321ad7d8108dc6))


### Feature

* feat: Include distance, represented in km, for satellite positions. ([`5d5a5b4`](https://github.com/NSF-Swift/satellite-overhead/commit/5d5a5b4e58b29a6918bbc92414172cca769f812b))


### Fix

* fix: Calculate orbits per day instead of orbital period and update filters to reflect for leo/meo/geo. ([`5ba4d45`](https://github.com/NSF-Swift/satellite-overhead/commit/5ba4d45a074d0484e70e35b14b858a9ddfeadaf5))


### Test

* test: Add test for orbits_per_day property on Satellite class. ([`ee60d1f`](https://github.com/NSF-Swift/satellite-overhead/commit/ee60d1ff4e1c533438e0c2d5567f3412608b9d56))



## v0.3.0 (2024-01-18)



## v0.2.0 (2024-01-18)


### Build

* build: correctly name Publish action. ([`6dbfe16`](https://github.com/NSF-Swift/satellite-overhead/commit/6dbfe1683e43e4f858d6f5dbdb936b12111f665e))

* build: Add ci/cd pass/fail badge to README. ([`adf0bd1`](https://github.com/NSF-Swift/satellite-overhead/commit/adf0bd1e4ea5c862531fc665a24c9f55babfd50f))

* build: create CHANGELOG.md and GH Release note templates. ([`d4bfd1d`](https://github.com/NSF-Swift/satellite-overhead/commit/d4bfd1d7c2e51897f7900997e44e769498fee783))

* build: add version file. ([`f49a90e`](https://github.com/NSF-Swift/satellite-overhead/commit/f49a90ef7d3b30a70a9d25b2eece20e8eba260c3))

* build: use dynamic versioning. ([`325ee39`](https://github.com/NSF-Swift/satellite-overhead/commit/325ee393380ee98f6a96ef95ccea5e3c33337317))

* build: use psr to automatically version releases. ([`8e57945`](https://github.com/NSF-Swift/satellite-overhead/commit/8e5794544c7dad5aadfba67d909867872087d8da))


### Documentation

* docs: Update documentation to include information on satellite filtering. ([`65c8ddc`](https://github.com/NSF-Swift/satellite-overhead/commit/65c8ddcfe66634b3774dc8ce23aaa8bebe001434))


### Feature

* feat: Add set_satellites_filter function which takes a Filterer class with filters to later filter the list of satellites based on the applied filters. ([`bbbcf67`](https://github.com/NSF-Swift/satellite-overhead/commit/bbbcf672affb24fb777b51e9df5c6f24dc037bc6))

* feat: Add orbital_period property to Satellite class which provides the orbital period in minutes. ([`f8fb8f2`](https://github.com/NSF-Swift/satellite-overhead/commit/f8fb8f2c294c928af72269cc369b7ad59697c059))

* feat: add ConfigurationBuilder to easily create Configuration objects ([`8301e30`](https://github.com/NSF-Swift/satellite-overhead/commit/8301e30475d5084a69f27ef81e49bece8b03bb42))


### Fix

* fix: resolve error where datetime strings without microsencs caused an error ([`fe65b13`](https://github.com/NSF-Swift/satellite-overhead/commit/fe65b135c7e5d55d392670e4b2ff7baec5e07e8f))


### Refactor

* refactor: Rename dir to satellites_filter. ([`a4851b5`](https://github.com/NSF-Swift/satellite-overhead/commit/a4851b52aaa67995cb630e26a82b60b120265bf2))

* refactor: Rename geo/leo/meo filters to be clearer. ([`d5c380f`](https://github.com/NSF-Swift/satellite-overhead/commit/d5c380f4098de1c1ee923f9570eaabfbffaad4fc))

* refactor: Change filter name to name_does_not_contain_filter for clarity. ([`df2dac6`](https://github.com/NSF-Swift/satellite-overhead/commit/df2dac69fa7dda9031dda39bdb1cc29bc49552c4))

* refactor: Use a generic filtering strategy. ([`2bdb59f`](https://github.com/NSF-Swift/satellite-overhead/commit/2bdb59fb871163bb9b55e4adb8cf01038a1cb86b))

* refactor: Update Main() to use refactored frequency filter. ([`01e92d9`](https://github.com/NSF-Swift/satellite-overhead/commit/01e92d9d708a55fabe0f267c27227954b5cc38a0))


### Style

* style: fix whitespace. ([`0624af9`](https://github.com/NSF-Swift/satellite-overhead/commit/0624af98efc88bdc10658bfa2efd9e0ace4395ab))


### Test

* test: Add tests for satellites filtering ([`51432b0`](https://github.com/NSF-Swift/satellite-overhead/commit/51432b061b20ae95c76b695ddf879a637625daa9))

* test: Add tests for refactored filtering strategy. ([`eec6b83`](https://github.com/NSF-Swift/satellite-overhead/commit/eec6b83306f030ec926778d14f50456e0817d5de))

* test: Update tests to use refactored frequency filter. ([`3b47f7c`](https://github.com/NSF-Swift/satellite-overhead/commit/3b47f7c8d70aa2a86976bf60964d83085205590a))

* test: Update tests to account for filtering refactor. ([`edeede3`](https://github.com/NSF-Swift/satellite-overhead/commit/edeede30ef6f160dfc75c044df98b35889dd312d))



## v0.1.0 (2024-01-10)

