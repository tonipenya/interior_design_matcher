from io import BytesIO
import ipywidgets as widgets
from keras.preprocessing.image import img_to_array, array_to_img
from IPython.display import display

def resize_and_normalize_image(img_array, size_x, size_y):
    img = array_to_img(img_array).resize((size_x, size_y))
    img_array = img_to_array(img) / 255
    return img_array

def resize_image(img_array, size_x, size_y):
    img = array_to_img(img_array).resize((size_x, size_y))
    return img_to_array(img)

def mirror_image(img_array):
    img = array_to_img(img_array)
    img = ImageOps.mirror(img)

    return img_to_array(img)

def crop_image(img_array, corner):
    img = array_to_img(img_array)
    width, height = img.size
    corners = {
        'top_left': (0,0,width/2, height/2),
        'top_right': (width/2,0,width, height/2),
        'bottom_left': (0,height/2,width/2, height),
        'bottom_right': (width/2, height/2, width, height)
    }

    min_size = min(width, height)

    return img.crop(corners[corner]).resize((min_size, min_size))

def jpeg_bytes_from_nparray(array):
    b = BytesIO()
    array_to_img(array).save(b, 'jpeg')
    return b.getvalue()

def resize_and_normalize_image(img_array, size_x, size_y):
    img = array_to_img(img_array).resize((size_x, size_y))
    img_array = img_to_array(img) / 255
    return img_array

def add_normalized_column(dataframe, width, height, from_col='original', to_col='normalized'):
    dataframe[to_col] = dataframe[from_col].map(lambda x: resize_and_normalize_image(x, width, height))

def mirrored_version(dataframe):
    print 'orig %d' % dataframe.shape[0]
    df2 = dataframe.copy()
    print 'copy %d' % df2.shape[0]
    df2.original = df2.original.map(lambda x: mirror_image(x))
    print 'mirror %d' % df2.shape[0]
    add_normalized_column(df2)
    print 'normal %d' % df2.shape[0]
    df2['tranformation'] = 'mirror'
    print 'label %d' % df2.shape[0]
    return df2

def cropped_version(dataframe):
    df_top_left = dataframe.copy()
    df_top_right = dataframe.copy()
    df_bot_left = dataframe.copy()
    df_bot_right = dataframe.copy()

    df_top_left.original = df_top_left.original.map(lambda x: crop_image(x, 'top_left'))
    df_top_right.original = df_top_right.original.map(lambda x: crop_image(x, 'top_right'))
    df_bot_left.original = df_bot_left.original.map(lambda x: crop_image(x, 'bottom_left'))
    df_bot_right.original = df_bot_right.original.map(lambda x: crop_image(x, 'bottom_right'))

    df2 = pd.concat([df_top_left, df_top_right, df_bot_left, df_bot_right])
    add_normalized_column(df2)
    df2['transformation'] = 'crop'
    return df2

def show_photos(images):
    w = widgets.Box(
        [
            widgets.Image(
                value=jpeg_bytes_from_nparray(img_array),
                width='300px',
            ) for img_array in images
        ],
        layout=widgets.Layout(display='flex', flex_flow='row wrap', justify_content='space-around', align_items='flex-end')
    )

    display(w)
