# edge-mqtt-filter

<a href="https://www.buymeacoffee.com/mulrex" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>


### Introduction

The purpose of this script is to read mqtt messages from a single endpoint and then forward those requests to a more precise mqtt endpoint for homebridge. In doing so this eliminates the issue of having to decode the payload (base64, cayenne lpp), and cycle through the mqtt payload for a single deveui (extremely difficult in the current implementation of mqttthing-homebridge)
