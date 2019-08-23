##############
# Created by Eric Davidson
# Generate structures built from cubes (or slabs) with Perlin noise
##############


# Dimensions of the structure
grid_height = 70
grid_width = 70

# Customize the basic block
block_size = 20
block_height = 10
lines = 5
sw = 2

# Adjust the parameters affecting perlin noise
noise_scale = .05
noise_multiplier = 100
noise_dampener = 2

# Eventually multiplied by block size
image_border_buff = 5


# Important (and fragile) code used to center the structure based on block size
#################
w = grid_width * block_size + grid_height * block_size + image_border_buff * block_size
h = grid_height * block_size/2 + grid_width * block_size/2 + (int(noise(0, 0) * noise_multiplier) / noise_dampener * block_height) + image_border_buff * block_size

start_block_x = w/2 - grid_height/2 * block_size + grid_width/2 * block_size
start_block_y = h/2 - grid_height/2 * block_size/2 - grid_width/2 * block_size/2 + (int(noise(0, 0) * noise_multiplier) / noise_dampener * block_height/2)
#################


# Preload any input image
def preload():
    img = loadImage("/Input/flatter.png")

# Basic Block, centered on top face
def draw_block(x, y):
    beginShape()
    
    # Top Face
    vertex(x - block_size, y)
    vertex(x, y - block_size/2)
    vertex(x + block_size, y)
    vertex(x, y + block_size/2)
    endShape(CLOSE)
    
    # Left Face
    beginShape()
    vertex(x - block_size, y)
    vertex(x, y + block_size/2)
    vertex(x, y + block_height + block_size/2)
    vertex(x - block_size, y + block_height)
    endShape(CLOSE)
    
    #Add lines to left face (Helps with depth)
    line_sep = block_height/lines
    for l in range(lines):
        line(x - block_size, y + (l * line_sep), x, y + block_size/2 + (l * line_sep))
    
    # Right Face
    beginShape()
    vertex(x + block_size, y)
    vertex(x, y + block_size/2)
    vertex(x, y + block_height + block_size/2)
    vertex(x + block_size, y + block_height)
    endShape(CLOSE)
    
    
def setup():
    img = loadImage("Input/flatter.png")
    
    img.loadPixels()
    
    x_inc = img.width/grid_width
    y_inc = img.height/grid_height
    
    height_grid = []
    
    # size(4000, 4000)
    
    # Loop through image in squares, average color, determine luminosity
    for x in range(0, img.width - x_inc, x_inc):
        for y in range(0, img.height - y_inc, y_inc):
            
            # Get the average color for square
            counter = 0
            red_total = 0
            green_total = 0
            blue_total = 0
            
            # Get color value for each pixel in square
            for i in range(0, x_inc):
                for j in range(0, y_inc):
                    p = img.pixels[(x + y * img.width) + (i + j * img.width)]
                    red_total += red(p)
                    green_total += green(p)
                    blue_total += blue(p)
                    counter += 1
            
            # Color average of square
            average = (red_total/counter, green_total/counter, blue_total/counter)
            
            # Convert color average to luminance
            lum = (average[0] * .2126) + (average[1] * .7152) + (average[2] * .0722)
            height_grid.append(lum)
            
            fill(lum)
            rect(x, y, x + x_inc, y + y_inc)
    

    size(w, h)
    # Need to extract to variable
    background(190, 194, 249)
    
    # Take advantage of screen resolution
    pixelDensity(2)
    
    # # Width of lines
    # strokeWeight(sw)

    # Color of cubes
    fill(254, 171, 227)
    
    # Debugging for centering structure
    # line(w/2, 0, w/2, h)
    # line(0, h/2, w, h/2)
    
    # Draw each cube
    for x in range(grid_height):
        print(x)
        for y in range(grid_width):
            
            # Generate Perlin Noise and normalize
            cubes = height_grid[y + x * grid_height] / 10
            
            # Use normalized perlin noise to generate towers
            for i in range(int(cubes)):
                draw_block((start_block_x + x*block_size) - y*block_size, (start_block_y + x*(block_size/2)) + y*(block_size/2) - i*(block_height))
    
    # Save to example folder
    # save('Examples/Vapor/' + str(grid_height) + '-' + str(grid_width) + '.png')
    save('Examples/test.png')
    
