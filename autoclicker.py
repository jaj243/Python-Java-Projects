#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pyautogui

# Set the number of clicks you want to simulate
num_clicks = 100

# Set the duration (in seconds) between clicks
click_interval = 0.5

# Set the button you want to simulate clicks on (e.g. left click, right click)
button = 'left'

# Use a for loop to simulate the clicks
for i in range(num_clicks):
    pyautogui.click(button=button)
    pyautogui.sleep(click_interval)

