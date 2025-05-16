# vecteditor is a simple vector graphics editor
# it allows you to create and edit vector animations and export them as PNG spritesheets
# shapes move automatically on a timescale from position A to position B that is preset by the user
# images can be exported as low-frame rate PNG spritesheets or as high-frame rate PNG spritesheets
# lower frame rate reduces lag on low-end devices

import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VectEditor")

clock = pygame.time.Clock()
running = True

# Define some colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Store shapes as a list of dictionaries
shapes = []

# Drawing state
drawing = False
start_pos = None
current_shape = None
selected_shapes = []  # Changed from selected_shape
editing_point = None  # (shape, point_index)

font = pygame.font.SysFont(None, 24)

def draw_shapes(surface, shapes, selected=None):
    for shape in shapes:
        color = shape['color']
        if selected and shape in selected:
            color = (255, 128, 0)  # Highlight selected shapes
        if shape['type'] == 'rect':
            pygame.draw.rect(surface, color, shape['rect'], 2)
        elif shape['type'] == 'ellipse':
            pygame.draw.ellipse(surface, color, shape['rect'], 2)
        elif shape['type'] == 'line':
            pygame.draw.line(surface, color, shape['start'], shape['end'], 2)

def get_shape_at_pos(pos):
    for shape in reversed(shapes):  # Topmost first
        if shape['type'] in ('rect', 'ellipse'):
            if pygame.Rect(shape['rect']).collidepoint(pos):
                return shape
        elif shape['type'] == 'line':
            # Simple hit test for line
            x1, y1 = shape['start']
            x2, y2 = shape['end']
            px, py = pos
            if min(x1, x2) - 5 <= px <= max(x1, x2) + 5 and min(y1, y2) - 5 <= py <= max(y1, y2) + 5:
                # Distance from point to line
                dx = x2 - x1
                dy = y2 - y1
                if dx == 0 and dy == 0:
                    continue
                t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
                t = max(0, min(1, t))
                nearest = (x1 + t * dx, y1 + t * dy)
                dist = ((nearest[0] - px) ** 2 + (nearest[1] - py) ** 2) ** 0.5
                if dist < 8:
                    return shape
    return None

# Tool selection
tools = ['rect', 'ellipse', 'line', 'move', 'point']  # Added 'move'
current_tool = 0  # 0=rect, 1=ellipse, 2=line, 3=move
tool_buttons = []  # Store button rects for tool selection

def draw_ui(surface):
    global tool_buttons
    tool_buttons = []
    # Draw tool buttons
    for i, tool in enumerate(tools):
        rect = pygame.Rect(10 + i * 90, 5, 80, 28)
        tool_buttons.append(rect)
        color = (200, 200, 200) if i == current_tool else (230, 230, 230)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 2)
        label = font.render(tool.capitalize(), True, (0, 0, 0))
        surface.blit(label, (rect.x + 10, rect.y + 4))
    instr = font.render("LMB: Draw/Move | RMB: Select | Del: Delete | S: Save PNG", True, (0, 0, 0))
    surface.blit(instr, (10, 35))

def save_screenshot():
    pygame.image.save(screen, "vecteditor_export.png")

move_offset = None

def draw_checkerboard(surface, cell_size=40):
    color1 = (107, 107, 107)
    color2 = (147, 147, 147)
    rows = HEIGHT // cell_size + 1
    cols = WIDTH // cell_size + 1
    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if (x + y) % 2 == 0:
                pygame.draw.rect(surface, color1, rect)
            else:
                pygame.draw.rect(surface, color2, rect)

def draw_point_handles(surface, shape):
    handle_color = (0, 0, 0)
    handle_radius = 6
    if shape['type'] in ('rect', 'ellipse'):
        rect = shape['rect']
        points = [
            (rect.left, rect.top),
            (rect.right, rect.top),
            (rect.right, rect.bottom),
            (rect.left, rect.bottom)
        ]
    elif shape['type'] == 'line':
        points = [shape['start'], shape['end']]
    else:
        return
    for pt in points:
        pygame.draw.circle(surface, handle_color, pt, handle_radius)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                current_tool = (current_tool + 1) % len(tools)
            elif event.key == pygame.K_DELETE and selected_shapes:
                for shape in selected_shapes:
                    if shape in shapes:
                        shapes.remove(shape)
                selected_shapes = []
            elif event.key == pygame.K_s:
                save_screenshot()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            ctrl_held = pygame.key.get_mods() & pygame.KMOD_CTRL
            # Tool button selection
            if event.pos[1] <= 33:  # UI area
                for i, rect in enumerate(tool_buttons):
                    if rect.collidepoint(event.pos):
                        current_tool = i
                        break
            elif event.button == 1:  # Left click
                if tools[current_tool] == 'move' and selected_shapes:
                    # Start moving the last selected shape
                    shape = selected_shapes[-1]
                    if shape['type'] in ('rect', 'ellipse'):
                        move_offset = (event.pos[0] - shape['rect'].x, event.pos[1] - shape['rect'].y)
                    elif shape['type'] == 'line':
                        move_offset = (event.pos[0] - shape['start'][0], event.pos[1] - shape['start'][1])
                elif tools[current_tool] == 'point' and selected_shapes:
                    shape = selected_shapes[-1]
                    # Check if a handle is clicked
                    handles = []
                    if shape['type'] in ('rect', 'ellipse'):
                        rect = shape['rect']
                        handles = [
                            (rect.left, rect.top),
                            (rect.right, rect.top),
                            (rect.right, rect.bottom),
                            (rect.left, rect.bottom)
                        ]
                    elif shape['type'] == 'line':
                        handles = [shape['start'], shape['end']]
                    mx, my = event.pos
                    for idx, (hx, hy) in enumerate(handles):
                        if (mx - hx) ** 2 + (my - hy) ** 2 < 8 ** 2:
                            editing_point = (shape, idx)
                            break
                else:
                    if not drawing:
                        drawing = True
                        start_pos = event.pos
                        if tools[current_tool] == 'rect':
                            current_shape = {'type': 'rect', 'rect': pygame.Rect(start_pos, (0, 0)), 'color': RED}
                        elif tools[current_tool] == 'ellipse':
                            current_shape = {'type': 'ellipse', 'rect': pygame.Rect(start_pos, (0, 0)), 'color': BLUE}
                        elif tools[current_tool] == 'line':
                            current_shape = {'type': 'line', 'start': start_pos, 'end': start_pos, 'color': GREEN}
            elif event.button == 3:  # Right click: select (no move)
                shape = get_shape_at_pos(event.pos)
                if shape:
                    if ctrl_held:
                        if shape in selected_shapes:
                            selected_shapes.remove(shape)
                        else:
                            selected_shapes.append(shape)
                    else:
                        selected_shapes = [shape]
                else:
                    if not ctrl_held:
                        selected_shapes = []

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if tools[current_tool] == 'move':
                    move_offset = None
                elif drawing:
                    drawing = False
                    if current_shape:
                        # Only add if shape has size
                        if current_shape['type'] in ('rect', 'ellipse'):
                            if current_shape['rect'].width > 5 and current_shape['rect'].height > 5:
                                shapes.append(current_shape)
                        elif current_shape['type'] == 'line':
                            if current_shape['start'] != current_shape['end']:
                                shapes.append(current_shape)
                        current_shape = None
            elif event.button == 3:
                move_offset = None
            if tools[current_tool] == 'point':
                editing_point = None

        elif event.type == pygame.MOUSEMOTION:
            if tools[current_tool] == 'move' and move_offset and selected_shapes:
                mx, my = event.pos
                # Only move the last selected shape
                shape = selected_shapes[-1]
                if shape['type'] in ('rect', 'ellipse'):
                    shape['rect'].x = mx - move_offset[0]
                    shape['rect'].y = my - move_offset[1]
                elif shape['type'] == 'line':
                    dx = mx - move_offset[0] - shape['start'][0]
                    dy = my - move_offset[1] - shape['start'][1]
                    shape['start'] = (shape['start'][0] + dx, shape['start'][1] + dy)
                    shape['end'] = (shape['end'][0] + dx, shape['end'][1] + dy)
                move_offset = (mx - (shape['rect'][0] if 'rect' in shape else shape['start'][0]),
                               my - (shape['rect'][1] if 'rect' in shape else shape['start'][1]))
            elif drawing and current_shape:
                if current_shape['type'] in ('rect', 'ellipse'):
                    x0, y0 = start_pos
                    x1, y1 = event.pos
                    rect = pygame.Rect(min(x0, x1), min(y0, y1), abs(x1 - x0), abs(y1 - y0))
                    current_shape['rect'] = rect
                elif current_shape['type'] == 'line':
                    current_shape['end'] = event.pos
            elif tools[current_tool] == 'point' and editing_point:
                shape, idx = editing_point
                mx, my = event.pos
                if shape['type'] in ('rect', 'ellipse'):
                    rect = shape['rect']
                    # Get current corners
                    points = [
                        [rect.left, rect.top],
                        [rect.right, rect.top],
                        [rect.right, rect.bottom],
                        [rect.left, rect.bottom]
                    ]
                    points[idx] = [mx, my]
                    # Only update the moved corner, keep the other corners fixed
                    # Rebuild rect from new points (bounding box of all corners)
                    xs = [pt[0] for pt in points]
                    ys = [pt[1] for pt in points]
                    new_rect = pygame.Rect(min(xs), min(ys), max(xs)-min(xs), max(ys)-min(ys))
                    shape['rect'] = new_rect
                elif shape['type'] == 'line':
                    if idx == 0:
                        shape['start'] = (mx, my)
                    else:
                        shape['end'] = (mx, my)

    screen.fill((255, 255, 255))  # White background

    # Draw checkerboard background
    draw_checkerboard(screen)

    draw_shapes(screen, shapes, selected_shapes)
    if current_shape:
        draw_shapes(screen, [current_shape])
    if tools[current_tool] == 'point' and selected_shapes:
        draw_point_handles(screen, selected_shapes[-1])

    draw_ui(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
