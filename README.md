This is a small project to turn my reMarkable 2 into linux graphics tablet.
I tried to use [remouse](https://github.com/Evidlo/remarkable_mouse) in the past, but for some reason (perhaps my trashy laptop) it was very laggy, so here is my solution.
Script was tested and works on Debian/Sway. On Arch/Hyprland there are some issues (see notes).

### Dependancies

This script uses [goMarkableStream](https://github.com/owulveryck/goMarkableStream) to get pen data from the tablet, as well as [`uinput`](https://pypi.org/project/python-uinput/) library in order to create virtual mouse device.

### Notes
In order to match tablet with specific monitor run
```bash
swaymsg input 0:0:Virtual_Mouse/Tablet map_to_output "$DEVICE"
```
where `$DEVICE` is the name of your monitor.

On Hyprland mapping is not (yet?) possible: virtual device registers as a mouse,
and Hyprland does not allow mapping mice to single output.
I'm unable to register virtual device in a way hyprctl recognizes it as a tablet.
