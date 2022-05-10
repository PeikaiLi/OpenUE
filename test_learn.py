"""Experiment-running framework."""
import argparse
import importlib

import numpy as np
import torch
import pytorch_lightning as pl
import openue.lit_models as lit_models
import yaml
import time
from openue.lit_models import MyTrainer
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


# In order to ensure reproducible experiments, we must set random seeds.


def _import_class(module_and_class_name: str) -> type:
    """Import class from a module, e.g. 'text_recognizer.models.MLP'"""
    module_name, class_name = module_and_class_name.rsplit(".", 1)
    module = importlib.import_module(module_name)
    class_ = getattr(module, class_name)
	
    return class_
    
    # x1.x2.x3.rsplit(".", 1) -> [x1.x2,x3]
    # x1.x2.x3.rsplit(".", 2) -> [x1,x2,x3]
    # rspitrsplit(".", n) 分割最后n个点的前后的数据,并拼接为list
    #字符串从右分割一次。
    # module_path,class_name = path.rsplit('.',maxsplit=1)
    # print('module_path-->',module_path)
    # print('class_name-->',class_name)
    # #下面相当于from func.hosts import disk
    # module = importlib.import_module(module_path)
    # #import_module反射，getattr(disk,'Disk'),disk 代表disk.py,Disk代表类
    # disk_class = getattr(module,class_name)
    # #实例化Disk类
    # JG=disk_class()
    # JG.run()
    # 这里
    # 下面相当于from module_name import class_name
    # module = importlib.import_module(module_name)
    # class_ = getattr(module, class_name)
    # #实例化Disk类
    # xxx = _class()
    # xxx.run() # 执行类方法



def _setup_parser():
    """Set up Python's ArgumentParser with data, model, trainer, and other arguments."""
    parser = argparse.ArgumentParser(add_help=False)

    # Add Trainer specific arguments, such as --max_epochs, --gpus, --precision
    trainer_parser = pl.Trainer.add_argparse_args(parser)
    trainer_parser._action_groups[1].title = "Trainer Args"  # pylint: disable=protected-access
    parser = argparse.ArgumentParser(add_help=False, parents=[trainer_parser])

    # # print(trainer_parser._action_groups[1].title == 'optional arguments') # True 改为了"Trainer Args"


    # Basic arguments
    parser.add_argument("--wandb", action="store_true", default=False)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--litmodel_class", type=str, default="SEQLitModel")
    parser.add_argument("--data_class", type=str, default="REDataset")
    parser.add_argument("--model_class", type=str, default="BertForRelationClassification")
    parser.add_argument("--load_checkpoint", type=str, default=None)

    # # parser.add_argument("--model_class", type=str, default="bert.BertForSequenceClassification") # 默认的这个不存在


    # Get the data and model classes, so that we can add their specific arguments
    temp_args, _ = parser.parse_known_args() 
    data_class = _import_class(f"openue.data.{temp_args.data_class}")
    model_class = _import_class(f"openue.models.{temp_args.model_class}")

    #  # parse_known_args() 作用方式很类似 parse_args() 但区别在于当存在额外参数时它不会产生错误。 
    #  # 而是会返回一个由两个条目构成的元组，其中包含带成员的命名空间和剩余参数字符串的列表。
    #  # print(temp_args.data_class)


    # Get data, model, and LitModel specific arguments
    data_group = parser.add_argument_group("Data Args")
    data_class.add_to_argparse(data_group)

    model_group = parser.add_argument_group("Model Args")
    model_class.add_to_argparse(model_group)

    lit_model_group = parser.add_argument_group("LitModel Args")
    lit_models.BaseLitModel.add_to_argparse(lit_model_group)

    # 在默认情况下，ArgumentParser 会在显示帮助消息时将命令行参数分为“位置参数”和“可选参数”两组。 
    # 当存在比默认更好的参数分组概念时，可以使用 add_argument_group() 方法来创建适当的分组:

    parser.add_argument("--help", "-h", action="help")
    return parser


def _save_model(litmodel, tokenizer, path):
    os.system(f"mkdir -p {path}")
    litmodel.model.save_pretrained(path)
    tokenizer.save_pretrained(path)
    litmodel.config.save_pretrained(path)

    # mkdir -p参数是能直接创建一个不存在的目录下的子目录



def main():

    parser = _setup_parser()
    args = parser.parse_args()
    print(args)




if __name__ == "__main__":

    main()
