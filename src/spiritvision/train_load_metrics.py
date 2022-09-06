import os
import argparse

from fastai.interpret import ClassificationInterpretation

import ai
import spiritvision as sv


def main(arguments):
    arch = int(arguments.arch)

    # batch size of 9 because of small dataset
    data_loader = ai.make_data_loader(sv.get_data_dir(), batch_size=9)

    learn = ai.resnet_learner(data_loader, arch)

    load_path = os.path.join(sv.get_models_dir(), f"resnet{arch}_model")
    learn.load(load_path)

    interp = ClassificationInterpretation.from_learner(learn)
    cm = interp.confusion_matrix()
    cm_png_path = os.path.join(sv.get_root_dir(), "confusion_matrix.png")

    ai.save_confusion_matrix_plot(confusion_matrix=cm, labels=data_loader.vocab, path=cm_png_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--arch', required=True, help="ResNet architecture. Choose from 18, 34 or 50")

    args = parser.parse_args()
    main(args)
