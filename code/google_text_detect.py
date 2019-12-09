from google.cloud import vision
import io
from enum import Enum
from PIL import Image, ImageDraw
import os

#img_path = './sproj_example_pics/Python_code_1.jpeg'
img_path = './sproj_example_pics/Python_code_2.jpeg'
#img_path = './sproj_example_pics/Java_code.jpeg'
#img_path = './sproj_example_pics/C_code.jpeg'
#img_path = './sproj_example_pics/red_helloworld.jpeg'
#img_path = './sproj_example_pics/linkedListFull.jpeg'
#img_path = './sproj_example_pics/queueFull.jpeg'
#img_path = './sproj_example_pics/table_full.jpeg'

output_prog = './output.py'


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def draw_bounds(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y], None, color)
    return image



def get_image_info(image_file, feature):
    """Returns document bounds given an image."""
    client = vision.ImageAnnotatorClient()

    bounds = []
    output_str = ''

    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    print('Word : {}'.format(word_text))
                    for symbol in word.symbols:
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)
                        if symbol.property.detected_break.type == 1:
                            output_str += symbol.text + ' '
                        elif symbol.property.detected_break.type == 3:
                            output_str += symbol.text + '\t'
                        elif symbol.property.detected_break.type == 5:
                            output_str += symbol.text + '\n'
                        else:
                            output_str += symbol.text

                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)

                if (feature == FeatureType.PARA):
                    bounds.append(paragraph.bounding_box)

            if (feature == FeatureType.BLOCK):
                bounds.append(block.bounding_box)

        if (feature == FeatureType.PAGE):
            bounds.append(block.bounding_box)

    print('-'*40)
    print('\n'+output_str)
    print('-'*40)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds, output_str


#def render_image_text(filein, fileout):
def render_image_text(filein):
    image = Image.open(filein)
    bounds, out_str = get_image_info(filein, FeatureType.PAGE)
    draw_bounds(image, bounds, 'blue')
    bounds, out_str = get_image_info(filein, FeatureType.PARA)
    draw_bounds(image, bounds, 'red')
    bounds, out_str = get_image_info(filein, FeatureType.WORD)
    draw_bounds(image, bounds, 'yellow')
    image.show()

    F = open(output_prog, 'a')
    F.write('\n'+out_str+'\n')
    F.close()

    os.system('code '+output_prog)



def main():

    render_image_text(img_path)


    """
    client = vision.ImageAnnotatorClient()

    with io.open(img_path, 'rb') as img_file:
        content = img_file.read()

    img = vision.types.Image(content=content)

    detect = client.document_text_detection(image=img)

    output_str = ''

    bounds = []

    for page in detect.full_text_annotation.pages:
        #print(page)
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    print('Word : {}'.format(word_text))
                    for symbol in word.symbols:
                        if symbol.property.detected_break.type == 1:
                            output_str += symbol.text + ' '
                        elif symbol.property.detected_break.type == 3:
                            output_str += symbol.text + '\t'
                        elif symbol.property.detected_break.type == 5:
                            output_str += symbol.text + '\n'
                        else:
                            output_str += symbol.text
                        print('\tSymbol: {}'.format(symbol.text))

    print('-'*40)
    print('\n'+output_str)
    print('-'*40)

    for page in detect.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                print('\tParagraph confidence: {}'.format(paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    print('\t\tWord text: {} (confidence: {})'.format(word_text, word.confidence))

                    for symbol in word.symbols:
                        print('\t\t\tSymbol: {} (confidence: {})'.format(symbol.text, symbol.confidence))
    """
    return

if __name__ == '__main__':
    main()