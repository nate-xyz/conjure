<img src="/data/icons/icon.svg" align="left" height="250px" vspace="10px">

Conjure
======

Magically transform your images with Conjure. 
Resize, crop, rotate, flip images, apply various filters and effects, adjust levels and brightness, and much more.
An intuitive tool for designers, artists, or just someone who wants to enhance their images.

Built on top of the popular image processing library, [ImageMagick](https://github.com/ImageMagick/ImageMagick) with python bindings from [Wand](https://github.com/emcconville/wand).

<br><br>

![Screenshot 0](./data/screenshots/conjure-0.png)

Flatpak
--------------

You can install stable builds of Conjure from [Flathub](https://flathub.org)
by using this command:

    flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
    flatpak install flathub io.github.nate_xyz.Conjure

<a href="https://flathub.org/apps/details/io.github.nate_xyz.Conjure"><img src="https://flathub.org/assets/badges/flathub-badge-en.png" width="200"/></a>

## Nix
### The easiest way to install package

Install `nix` package manager:
```bash
sh <(curl -L https://nixos.org/nix/install) --daemon
```

Add `unstable` channel:
```bash
nix-channel --add https://nixos.org/channels/nixpkgs-unstable unstable
nix-channel --update
```
Install `conjure` package:
```bash
nix-env -iA unstable.conjure
```
Run:
```bash
conjure
```
### The best way to install package

If you want the best experience and all the features of nix, you need to follow a few steps described in [this](https://github.com/sund3RRR/nix-on-generic-linux) repository.

Screenshots
--------------
![Screenshot 1](./data/screenshots/conjure-1.png)
![Screenshot 2](./data/screenshots/conjure-2.png)