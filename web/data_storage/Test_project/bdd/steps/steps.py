# -*- coding: utf-8 -*-
from behave import *
from selenium.webdriver.support.ui import WebDriverWait
import time

@given('we have behave installed')
def step_impl(context):
	pass

@when('we implement {number:d} tests')
def step_impl(context, number):  # -- NOTE: number is converted into integer
	assert number > 1 or number == 0
	context.tests_count = number

@then('behave will test them for us!')
def step_impl(context):
	assert context.failed is False
	assert context.tests_count >= 0

@then('behave will test it for us!')
def step_impl(context):
    assert context.failed is False
    assert context.tests_count >= 0

@given(u'открыта главная страница')
def step_impl(context):
    url = context.get_project().make_full_url('/')
    context.get_browser().get(url)

@then(u'на странице должен быть заголовок {should_text}')
def step_impl(context,should_text):
    element = context.get_browser().find_element_by_tag_name('h3')
    print ("(",element.text,")","(",should_text,")")
    assert element.text == should_text

@then(u'не должно быть текста {should_not_text}')
def step_impl(context,should_not_text):
    assert not should_not_text in context.get_browser().page_source

@when(u'сделать что-нибудь')
def step_impl(context):
    pass

@when(u'сделать еще что-нибудь')
def step_impl(context):
    pass

@then(u'должен получиться какой-то результат')
def step_impl(context):
    pass

@given(u'приложение находится в состоянии "{app_state}"')
def step_impl(context,app_state):
    pass

@when(u'сделать действие с параметром "{param}"')
def step_impl(context,param):
    pass

@then(u'в результате должно быть "{result}"')
def step_impl(context,result):
    assert result != 'result_example2'
    pass

@when(u'я открою страницу {page}')
def step_impl(context,page):
    url = context.get_project().make_full_url(page)
    context.get_browser().get(url)