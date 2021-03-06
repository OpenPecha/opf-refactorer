import shutil
import time
import logging
from git import Repo
from pathlib import Path
from github import Github
from openpecha.utils import load_yaml


logging.basicConfig(
    filename="Deleted_pechas.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
)


config = {
    "OP_ORG": "https://github.com/Openpecha-Data"
}


def clean_dir(layers_output_dir):
    if layers_output_dir.is_dir():
            shutil.rmtree(str(layers_output_dir))


def notifier(msg):
    logging.info(msg)


def check_new_pecha(pecha_id, g):
    repo = g.get_repo(f"Openpecha-Data/{pecha_id}")
    contents = repo.get_contents(f"./{pecha_id}.opf/meta.yml")
    if contents != None:
        return True
    else:
        return False
    
    
def _get_openpecha_org(org_name, g):
    """OpenPecha github org singleton."""
    org = g.get_organization(org_name)
    return org

    
def delete_repo_from_github(pecha_id, g):
    org = _get_openpecha_org("Openpecha-Data", g)
    repo = org.get_repo(pecha_id)
    repo.delete()
    notifier(f"{pecha_id} is deleted from github")
        
def clean_old_pechas(ids_path, pecha_dic_path, g):
    pecha_dic = load_yaml(pecha_dic_path)
    pecha_ids = (ids_path.read_text(encoding='utf-8')).splitlines()
    for num, pecha_id in enumerate(pecha_ids, 1):
        if num > 3803 :
            new_pecha =  pecha_dic[pecha_id]
            check = check_new_pecha(new_pecha, g)
            if check ==True:
                delete_repo_from_github(pecha_id, g)
                print(f"{pecha_id} is deleted")
                time.sleep(20)
            else:
                notifier(f"{pecha_id} is not deleted")

def clean_new_pechas(ids_path, g):
    pecha_ids = (ids_path.read_text(encoding='utf-8')).splitlines()
    for pecha_id in pecha_ids:
        delete_repo_from_github(pecha_id, g)
        print(f"{pecha_id} is deleted")
        time.sleep(20)
            
if __name__ == "__main__":
    token = "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"
    g = Github(token)
    pecha_dic_path = Path(f"./clean_openpecha-data_github/pecha_dic.yml")
    old_pecha_path = Path(f"./clean_openpecha-data_github/old_pecha_delete_list.txt")
    new_pecha_path = Path(f"./clean_openpecha-data_github/new_pecha_delete_list.txt")
    clean_old_pechas(old_pecha_path, pecha_dic_path, g)
    clean_new_pechas(new_pecha_path, g)
    
    
    
    
    # P009289
    # P010621
    # P001856
    
    
    
    
    # not deleted due to error
    # P000316
    # P000369
    # P000525
    # P000457
    # P000806