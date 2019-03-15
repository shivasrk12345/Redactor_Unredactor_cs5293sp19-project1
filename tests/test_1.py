import pytest
import glob

from project1 import project1
totaldata=[]
def test_readdata():
    totaldata=project1.readfiles('project1/testingtexts/*.txt')
    assert totaldata is not None
def test_namedentities():
    text,x=project1.get_redactednameentities(totaldata)
    assert text is not None
def test_genders():
    text=project1.extact_genders(totaldata)
    assert text is not None
def test_dates():
    #totaldata=project1.readfiles()
    text=project1.extractdates(totaldata)
    assert text is not None
def test_phones():
    #totaldata=project1.readfiles()
    text=project1.extract_phonenumbers(totaldata)
    assert text is not None

