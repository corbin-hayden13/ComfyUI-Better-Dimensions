## Install

1. Open you command console in the `custom_nodes` directory
2. Clone the repository to `custom_nodes` with `git clone https://github.com/corbin-hayden13/ComfyUI-Better-Dimensions.git`
3. Reload ComfyUI

## Nodes and Usage

### Better Image Dimensions

The most versatile node that allows you to set your own width and height while giving you access to the common image ratios that will automatically adjust either your width or height (user choice as "enforce_dimension") to stay within your desired ratio. You can also choose to not use a ratio. Furthermore, you can easily swap between landscape and portrait mode by choosing the order of output, defaulting to width x height. Choosing the swap option will swap the two values to height x width so you don't have to reconnect your nodes over again.

### Standard SDXL Dimensions node

Comes pre-loaded with recommended SDXL dimensions so you don't have to look them up. It also features the ability to switch between landscape and portrait mode by swapping the order of the outputs.

### Dimensions by Ratio node

If you're not concerned about the actual pixel values but instead want to fit into a specific ratio, this is for you. You can choose a ratio then scale the image up or down using the "adjust_scale" value. Because SDXL is base 1024 and SD 1.5 is base 512, there's an option to choose which model you're using so the ratio creates width and height values at the appropriate base. This node again supports the ability to swap your width and height.