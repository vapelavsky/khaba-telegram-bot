import os

from pptx import Presentation
from pptx.util import Inches
from db.config import BASE_DIR
from celery import Celery

app = Celery()


@app.task
def create_presentation(name, image_list, faculty):
    prs = Presentation()
    steps = [Inches(1), Inches(4), Inches(6.5)]
    for i in range(len(image_list)):
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        title_shape = slide.shapes.title
        title_shape.text = name[i]
        for image in image_list[i]:
            left = steps[image_list[i].index(image)]
            top = Inches(2)
            width = Inches(3)
            height = Inches(3)
            img = slide.shapes.add_picture(image, left, top, width, height)

    prs.save(os.path.join(BASE_DIR, f'presentations/{faculty}_report.pptx'))


if __name__ == '__main__':
    app.worker_main()
