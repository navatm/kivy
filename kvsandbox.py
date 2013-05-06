#!/usr/bin/env python
'''
'''

import re

import kivy
import os
kivy.require('1.6.1')

from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty

Builder.load_string('''
#:import psplit os.path.split

<FileDialog>:
	filename_input: filename_input
	
	BoxLayout:
		size: root.size
		pos: root.pos
		orientation: 'vertical'
		
		BoxLayout:
			size_hint_y: None
			height: 30
			
			Label:
				id: error
				bold: True
				text: root.error
		
		FileChooserIconView:
			id: filechooser
			filters: ['*.kv']
			path: root.path
			on_selection: filename_input.text = self.selection and psplit(self.selection[0])[-1] or ''
		
		BoxLayout:
			size_hint_y: None
			height: dp(32)
			
			Label:
				text: 'Filename'
				size_hint_x: 0.2
			
			TextInput:
				id: filename_input
				text: root.filename
		
		BoxLayout:
			size_hint_y: None
			height: 30
			Button:
				text: "Cancel"
				on_release: root.cancel()
			
			Button:
				text: root.intent
				on_release: root.action(path=filechooser.path, selection=filechooser.selection, filename=filename_input.text)
''')

class FileDialog(FloatLayout):
	intent = StringProperty('')
	action = ObjectProperty(None)
	cancel = ObjectProperty(None)
	error = StringProperty('')
	path = StringProperty(os.curdir)
	filename = StringProperty('')

class Sandbox(FloatLayout):
	
	code = ObjectProperty(None)
	preview = ObjectProperty(None)
	valid = BooleanProperty(False)
	status = StringProperty('')
	
	popup_openfile = ObjectProperty(None)
	
	loaded = []
	
	re_include = re.compile(r'^#\s*include:\s*(.*)$', re.MULTILINE)
	
	last_path = None
	last_filename = None
	
	def on_code(self, *_):
		if self.loaded:
			for f in self.loaded:
				Builder.unload_file(f)
			self.loaded = []
		
		try:
			includes = self.re_include.findall(self.code.text)
			for f in includes:
				Builder.load_file(f)
				self.loaded += [f]
			widget = Builder.load_string(str(self.code.text), filename='sandboxstring.kv')
			self.loaded += ['sandboxstring.kv']
		except Exception, e:
			if self.code.text.find('#pdb') != -1:
				import sys
				tbinfo = sys.exc_info()
				try:
					from IPython.core import ultratb
					pdb = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=1)
				except:
					# IPython not available; untested code here!
					import pdb as pdb_module
					pdb_module.post_mortem(tbinfo[2])
				else:
					pdb(*tbinfo)
			self.set_status(e)
			widget = False
		
		if widget:
			self.set_preview(widget)
			self.valid = True
			self.set_status('')
		elif widget is None:
			if self.code.text:
				self.valid = False
				self.set_status('No root widget!')
			else:
				self.valid = True
				self.set_status('')
		else:
			self.valid = False
	
	def set_status(self, status):
		if not isinstance(status, basestring):
			status = repr(status)
		self.status = status.replace('\\n', '\n')
	
	def set_preview(self, widget):
		children = self.preview.children
		for child in children:
			self.preview.remove_widget(child)
		widget.pos_hint = {'top': 1.0}
		self.preview.add_widget(widget)
	
	def clear_code(self):
		self.set_preview(FloatLayout())
		self.code.text = ''
		self.last_filename = None
	
	def _open_dialog(self, intent, action):
		content = FileDialog(intent=intent, action=action, cancel=self.dismiss_popup, error='')
		content.path = self.last_path or content.path
		self._popup = Popup(title='{} File'.format(intent), content=content, size_hint=(0.8, 0.8))
		self._popup.open()
		return content
	
	def dismiss_popup(self):
		self._popup.dismiss()
	
	def open_file_dialog(self):
		self._open_dialog('Open', self.load_file)
	
	def load_file(self, path, selection, filename):
		if not selection:
			self._popup.error = 'No file selected!'
			return
		
		self.last_path = path
		
		filename = selection[0]
		if not os.path.exists(filename):
			self._popup.error = 'Invalid filename!'
			return
		
		self.last_filename = os.path.split(filename)[-1]
		
		try:
			kvstring = open(filename).read()
		except Exception, e:
			print '{}'.format(e)
			self._popup.error = 'Error reading file!'
			return
		
		self.code.text = kvstring
		self.set_status('Loaded file: {}'.format(filename))
		self.dismiss_popup()
	
	def save_file_dialog(self):
		dialog = self._open_dialog('Save', self.save_file)
		dialog.filename = self.last_filename or ''
	
	def save_file(self, path, selection, filename):
		if not filename:
			self._popup.error = 'No filename provided!'
			return
		
		self.last_path = path
		self.last_filename = filename
		filename = os.path.join(path, filename)
		
		try:
			with open(filename, 'w') as f:
				f.write(self.code.text)
		except Exception, e:
			print '{}'.format(e)
			self._popup.error = 'Error writing file!'
			return
		
		self.set_status('Saved file: {}'.format(filename))
		self.dismiss_popup()

root_widget = Builder.load_string('''
#:import KivyLexer kivy.extras.highlight.KivyLexer

Sandbox:
	code: code
	preview: preview
	
	BoxLayout:
		orientation: 'horizontal'
		BoxLayout:
			orientation: 'vertical'
			
			CodeInput:
				id: code
				auto_indent: True
				lexer: KivyLexer()
				on_text: root.on_code()
			
			BoxLayout:
				size_hint_y: None
				height: dp(64)
				
				Button:
					text: 'Open'
					on_press: root.open_file_dialog()
				
				Button:
					text: 'Save'
					on_press: root.save_file_dialog()
				
				Button:
					text: 'Clear'
					on_press: root.clear_code()
		
		RelativeLayout:
			BoxLayout:
				id: preview
				
				canvas.after:
					Color:
						rgba: (0.0, 0.0, 0.0, 0.0) if root.valid else (1.0, 0.9, 0.9, 0.2)
					Rectangle:
						pos: self.pos
						size: self.size
			
			Label:
				pos_hint: {'bottom': 1.0}
				size_hint: (1, None)
				text_size: self.width, None
				height: self.texture_size[1] if self.text else 0
				text: root.status
				color: [0.0, 0.0, 0.0, 1.0] if root.valid else [1.0, 0.0, 0.0, 1.0]
				canvas.before:
					Color:
						rgba: (0.0, 0.0, 0.0, 0.0) if root.valid else (1.0, 1.0, 1.0, 1.0)
					Rectangle:
						pos: self.pos
						size: self.size
				canvas.after:
					Color:
						rgba: (0.0, 0.0, 0.0, 0.0) if root.valid else (1.0, 0.3, 0.3, 1.0)
					Line:
						width: 1
						points: [self.pos[0], self.pos[1] + self.size[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]]
''')

from kivy.app import App

class SandboxApp(App):
	def build(self):
		return root_widget

if __name__ == '__main__':
	SandboxApp().run()
