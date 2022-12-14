from fastai.vision.all import *
from fastai.optimizer import ranger
from os import getcwd

currentDir = getcwd()
class Network:
  def __init__(self, mediaPath):

    self.mediaPath = Path(mediaPath)

    self.codes = ['lane', 'not lane']
    self.unlabeledPath = None
    self.learner = None
    self.dl = None

    self.void_code = {v:k for k,v in enumerate(self.codes)}['not lane']

    self.doPred()


  def doPred(self):
    self.setLearner()

  def cam_acc(self, inp, targ):
    targ = targ.squeeze(1)
    mask = targ != self.void_code
    return (inp.argmax(dim=1)[mask]==targ[mask]).float().mean()


  def setLearner(self, unlabeledPath = Path(currentDir + '/data/road/unlabeled'), opt = ranger):
    """Proces ladowania objektu learner odpowiedzialnego za stworzenie sieci DNN"""
    binary = DataBlock(blocks=(ImageBlock, MaskBlock(self.codes)),
                      get_items=get_image_files,
                      splitter=RandomSplitter(),
                      #  get_y=get_y,
                      item_tfms=Resize((250, 480)),
                      batch_tfms=[Normalize.from_stats(*imagenet_stats)])

    dls = binary.dataloaders(unlabeledPath, bs=4)
    self.learner = unet_learner(dls, resnet34, metrics=self.cam_acc, self_attention=True, act_cls=Mish, opt_func=opt)

    self.learner.load(currentDir + '/src/models/stage-1');
    self.dl = self.learner.dls.test_dl([self.mediaPath])

  def savePreds(self):
    """Proces wykonywania predykcji na podanym zdjeciu oraz zapisywanie go do pliku zdjeciowego predictedPhoto.png"""
    preds = self.learner.get_preds(dl=self.dl)

    pred_1 = preds[0][0]
    pred_arx = pred_1.argmax(dim=0)
    pred_arx = pred_arx.numpy()

    rescaled = (255.0 / pred_arx.max() * (pred_arx - pred_arx.min())).astype(np.uint8)
    im = Image.fromarray(rescaled)

    predictedPhotoPath = currentDir + '/photos/preds/predictedPhoto.png'

    im.save(predictedPhotoPath)

    return predictedPhotoPath

