##############
# Created by Eric Davidson
# Generate structures built from cubes (or slabs) with Perlin noise
##############


# Dimensions of the structure
grid_height = 30
grid_width = 30


# Customize the basic block
block_size = 10
block_height = 3
lines = 2
sw = 1

# Adjust the parameters affecting perlin noise
noise_scale = .05
noise_multiplier = 100
noise_dampener = 1

# Eventually multiplied by block size
image_border_buff = 15

# Gif Making
make_gif = False
iterations = 1

# Important (and fragile) code used to center the structure based on block size
#################
w = grid_width * block_size + grid_height * block_size + image_border_buff * block_size
h = grid_height * block_size/2 + grid_width * block_size/2 + (int(noise(0, 0) * noise_multiplier) / noise_dampener * block_height) + image_border_buff * block_size

start_block_x = w/2 - grid_height/2 * block_size + grid_width/2 * block_size
start_block_y = h/2 - grid_height/2 * block_size/2 - grid_width/2 * block_size/2 + (int(noise(0, 0) * noise_multiplier) / noise_dampener * block_height/2)
#################


# Basic Block, centered on top face
def draw_block(x, y, h):
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
    line_sep = float(block_height)/lines
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
    size(int(w), int(h))
    
    # Need to extract to variable
    background(255, 255, 255)
    
    # Take advantage of screen resolution
    pixelDensity(2)
    
    # Width of lines
    strokeWeight(sw)

    # Color of cubes
    # fill(254, 171, 227)
    
    # Debugging for centering structure
    # line(w/2, 0, w/2, h)
    # line(0, h/2, w, h/2)
    
    for g in range(iterations):
        # Draw each cube
        
        for x in range(grid_height):
            for y in range(grid_width):
                
                # Generate Perlin Noise and normalize
                cubes = int(noise((x + g) * noise_scale, y * noise_scale) * noise_multiplier) / noise_dampener
                
                # Use normalized perlin noise to generate towers
                # for i in range(int(cubes)):
                draw_block((start_block_x + x*block_size) - y*block_size, (start_block_y + x*(block_size/2)) + y*(block_size/2) - int(cubes)*(block_height), cubes)
        
        # Save to example folder
        if (make_gif == False):
            seed = int(random(10000))
            save('Examples/Vapor/' + str(seed) + '.png')
            print(seed)
        else:
            save('Examples/Test/' + str(g) + '.png')
        
