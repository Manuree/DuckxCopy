import flet as ft

import random
import string
import json
import os
import distutils
import sys
import time

def saveJsonFile(list, fileName, location):
    directory = resource_path(location)
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, fileName + ".json")
    with open(file_path, 'w') as f:
        json.dump(list, f)
        
def loadJsonFile(fileName, location):
    resources_directory = resource_path(location)
    json_file_path = os.path.join(resources_directory, fileName + ".json")
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as file:
            data = json.load(file)
            file.close()
    else:
        print("JSON file not found.")
    return data

def resource_path(relative_path):
    #relative_path = relative_path.replace("/", "\\")
    try:
        base_path = sys.MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    print(os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)

def id_generator(key:str):
    def num_generator():
        characters = string.digits + string.ascii_uppercase
        num = ''.join(random.choice(characters) for _ in range(6))
        return num
    if key == "TID":
        new_id = key + "_" + num_generator()
        while new_id in task_data["task"]:
            new_id = key + "_" + num_generator()
        return new_id
    elif key == "DTD":
        new_id = key + "_" + num_generator()
        while new_id in task_data["command"]:
            new_id = key + "_" + num_generator()
        return new_id
    elif key == "FTD":
        new_id = key + "_" + num_generator()
        while new_id in task_data["command"]:
            new_id = key + "_" + num_generator()
        return new_id

def copy(src, dst):
    try:
        distutils.dir_util.copy_tree(src, dst)
    except:
        page_overlay("Copy error", "alert")

def copy_file(scr, dst):
    if os.path.isdir(dst):
        _dst = os.path.join(dst, os.path.basename(scr))
    try:
        distutils.file_util.copy_file(scr, _dst)
        #shutil.copyfile(scr, dst)
        print(f"File copied from {scr} to {dst}")
        page_overlay(f"{scr} to {dst}", "message")
    except Exception as e:
        print(f"Error copying file: {e}")
        page_overlay(f"{scr} to {dst}", "message")


global task_data
try:
    task_data = loadJsonFile("task_data", resource_path("assets/resources"))
except:
    task_data = {
        "task":{
            "TID_NVZYI2":
            {
                "name":"New Task",
                "tag":"#ac92eb",
                "command":["DTD_20P094"]
            }
        },
        "command":{
            "DTD_20P094":
            {
                "source":"D:/",
                "destination":"D:/"
            }
        }
    }

# print(type(task_data["task"]["TID_NVZYI2"]["command"]))
# print(task_data["command"][task_data["task"]["TID_NVZYI2"]["command"][0]])

#Style
bd_radius = 4
bt_style_a = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=bd_radius))
palette_a = ["#F8985C", "#212A3E", "#03C988", "#e6125f", "#e1e6ec", "#006ad8", "#394867", "#43474e"]
palette_b = ["#ac92eb", "#4fc0e8", "#9ace63", "#f5c652", "#e45260"]
bt_icon_sacle_a = 0.7
#Style

class Command_DTD(ft.UserControl):
    def __init__(self, id, source, destination, remove_command):
        super().__init__()
        self.id = id
        self.source = source
        self.destination = destination
        self.remove_command = remove_command

    def build(self):
        def select_source_directory(e: ft.FilePickerResultEvent):
            if self.edit_path_col.visible == False:
                try:
                    path = self.source
                    path = os.path.realpath(path)
                    os.startfile(path)
                except:
                    print("No path")
                    page_overlay("Incorrect path", "alert")
            else:
                #page_overlay()
                try:
                    self.page.add(get_directory_source)
                    get_directory_source.get_directory_path("Select Directory")
                except:
                    print("Something Wrong! Please try again")
                    page_overlay("Something Wrong! Please try again", "alert")
               

        def get_source_directory_result(e: ft.FilePickerResultEvent):
            self.source = e.path if e.path else self.source
            self.edit_source_label.value = self.source
            self.page.remove(get_directory_source)
            self.update()
        
        def select_destination_directory(e: ft.FilePickerResultEvent):
            if self.edit_path_col.visible == False:
                try:
                    path = self.destination
                    path = os.path.realpath(path)
                    os.startfile(path)
                except:
                    print("No path")
                    page_overlay("Incorrect path", "alert")
            else:
                try:
                    self.page.add(get_directory_destination)
                    get_directory_destination.get_directory_path("Select Directory")
                except:
                    print("Something Wrong! Please try again")
                    page_overlay("Something Wrong! Please try again", "alert")

        def get_destination_directory_result(e: ft.FilePickerResultEvent):
            self.destination = e.path if e.path else self.destination
            self.edit_destination_label.value = self.destination
            self.page.remove(get_directory_destination)
            self.update()
        
        get_directory_source = ft.FilePicker(on_result=get_source_directory_result)
        get_directory_destination = ft.FilePicker(on_result=get_destination_directory_result)

        self.mode = None
        pull_bt = ft.ElevatedButton(text="PULL", bgcolor={ft.MaterialState.HOVERED: "#e6125f", "": "#279EFF"}, color="#F1F6F9",height=35, on_click=self.request, style=bt_style_a)
        push_bt = ft.ElevatedButton(text="PUSH", bgcolor={ft.MaterialState.HOVERED: "#e6125f", "": "#03C988"}, color="#F1F6F9",height=35, on_click=self.request, style=bt_style_a)
        self.source_label = ft.Text(value=self.source, color=palette_a[7], size=10)
        self.destination_label = ft.Text(value=self.destination, color=palette_a[7], size=10)
        self.edit_source_label = ft.TextField(value=self.source, color=palette_a[4], text_size=10, height=15,border_width=0, border_radius=2, content_padding=0, expand=True)
        self.edit_destination_label = ft.TextField(value=self.destination, color=palette_a[4], text_size=10, height=15,border_width=0, border_radius=2, content_padding=0, expand=True)
        s_folder_bt = ft.Container(ft.Row([ft.Icon(ft.icons.FOLDER, size=14, color="#1f7fce")]), on_hover=self.bt_hover_a, on_click=select_source_directory)
        d_folder_bt = ft.Container(ft.Row([ft.Icon(ft.icons.FOLDER, size=14, color="#01a26d")]), on_hover=self.bt_hover_a, on_click=select_destination_directory)
        self.del_bt = ft.Container(ft.Row([ft.Icon(ft.icons.DELETE, size=14, color=palette_a[4])]), on_click=self.self_remove, visible=False, on_hover=self.bt_hover_a)
        self.yes_bt = ft.Container(ft.Row([ft.Icon(ft.icons.CHECK, size=14, color=palette_a[2])]), on_click=self.edit_yes, visible=False, on_hover=self.bt_hover_a)
        self.cancel_bt = ft.Container(ft.Row([ft.Icon(ft.icons.CLOSE, size=14, color=palette_a[3])]), on_click=self.edit_cancel, visible=False, on_hover=self.bt_hover_a)
        path_icon_col = ft.Column([s_folder_bt, d_folder_bt], spacing=0)
        edit_icon_row = ft.Row([self.yes_bt, self.cancel_bt, self.del_bt], animate_size=ft.animation.Animation(200, ft.AnimationCurve.BOUNCE_OUT))
        self.view_path_col = ft.Column(controls=[self.source_label, self.destination_label], spacing=0)
        self.edit_path_col = ft.Column(controls=[self.edit_source_label, self.edit_destination_label], spacing=0, visible=False)
        path_col  = ft.Row([self.view_path_col, self.edit_path_col])
        path_row = ft.Row([path_icon_col, ft.Container(path_col, on_click=self.edit, expand=True), edit_icon_row], spacing=3)
        self.path_con = ft.Container(path_row, bgcolor="transparent", expand=True, border_radius=bd_radius, padding=ft.padding.only(left=5, top=2, right=5, bottom=2), height=35, border=ft.border.all(1, "#DDE6ED"))
        row = ft.Row(controls=[pull_bt, self.path_con, push_bt], spacing=5)
        return row
    
    def bt_hover_a(self, e):
        e.control.scale = 1.2 if e.control.scale == 1 else 1
        e.control.update()

    def request(self, e):
        if e.control.text == "PULL":
            self.mode = e.control.text = "PULL"
            copy(self.destination, self.source)
            page_overlay(f"{self.mode} to {self.source}", "message")
        elif e.control.text == "PUSH":
            self.mode = e.control.text = "PUSH"
            copy(self.source, self.destination)
            page_overlay(f"{self.mode} to {self.destination}", "message")
        
    
    def self_remove(self, e):
        del task_data["command"][self.id]
        self.remove_command(self, self.id)

    def edit(self, e):
        if self.edit_path_col.visible == False:
            self.view_path_col.visible = False
            self.edit_path_col.visible = True
            self.yes_bt.visible = True
            self.cancel_bt.visible = True
            self.del_bt.visible = True
            self.edit_source_label.value = self.source_label.value
            self.edit_destination_label.value = self.destination_label.value
            self.path_con.bgcolor = palette_a[6]
            self.update()
            print("Command Edit")
    
    def edit_yes(self, e):
        self.view_path_col.visible = True
        self.edit_path_col.visible = False
        self.yes_bt.visible = False
        self.cancel_bt.visible = False
        self.del_bt.visible = False
        self.source_label.value = self.edit_source_label.value
        self.destination_label.value = self.edit_destination_label.value
        self.path_con.bgcolor = "transparent"
        self.update()
        task_data["command"][self.id]["source"] = self.source_label.value
        task_data["command"][self.id]["destination"] = self.destination_label.value
        saveJsonFile(task_data, "task_data", resource_path("assets/resources"))
        print("Save")
        page_overlay("Save", "message")
    
    def edit_cancel(self, e):
        self.view_path_col.visible = True
        self.edit_path_col.visible = False
        self.yes_bt.visible = False
        self.cancel_bt.visible = False
        self.del_bt.visible = False
        self.path_con.bgcolor = "transparent"
        self.update()
        print("Cancel")

class Command_FTD(ft.UserControl):
    def __init__(self, id, mode, source, destination, remove_command):
        super().__init__()
        self.id = id
        self.mode = mode
        self.source = source
        self.destination = destination
        self.remove_command = remove_command

    def build(self):
        def select_file(e: ft.FilePickerResultEvent):
            if self.edit_path_col.visible == False:
                try:
                    path = self.source[0]
                    path = os.path.dirname(path)
                    path = os.path.realpath(path)
                    os.startfile(path)
                except:
                    print("No path")
                    page_overlay("Incorrect path", "alert")
            else:
                try:
                    self.page.add(filepicker)
                    filepicker.pick_files("Select file...", allow_multiple=True)
                except:
                    page_overlay("Something Wrong! Please try again", "alert")

        def return_file(e: ft.FilePickerResultEvent):
            self.page.remove(filepicker)
            self.source.clear()
            if e.files is not None:
                for i in range(len(e.files)):
                    self.source.append(e.files[i].path)
                print(self.source)
                self.render_files()
        
        def select_directory(e: ft.FilePickerResultEvent):
            if self.edit_path_col.visible == False:
                try:
                    path = self.destination
                    path = os.path.realpath(path)
                    os.startfile(path)
                except:
                    print("No path")
                    page_overlay("Incorrect path", "alert")
            else:
                try:
                    self.page.add(get_directory_dialog)
                    get_directory_dialog.get_directory_path("Select Directory")
                except:
                    page_overlay("Something Wrong! Please try again", "alert")

        def get_directory_result(e: ft.FilePickerResultEvent):
            self.destination = e.path if e.path else "Cancelled!"
            self.edit_destination_label.value = self.destination
            self.page.remove(get_directory_dialog)
            self.render_files()
        
        filepicker = ft.FilePicker(on_result=return_file)
        get_directory_dialog = ft.FilePicker(on_result=get_directory_result)

        self.pull_bt = ft.ElevatedButton(text="PULL", bgcolor={ft.MaterialState.HOVERED: "#e6125f", "": "#279EFF"}, color="#F1F6F9",height=35, on_click=self.request, style=bt_style_a)
        self.push_bt = ft.ElevatedButton(text="PUSH", bgcolor={ft.MaterialState.HOVERED: "#e6125f", "": "#03C988"}, color="#F1F6F9",height=35, on_click=self.request, style=bt_style_a)
        self.source_label = ft.Text(value=self.source, color=palette_a[7], size=10)
        self.destination_label = ft.Text(value=self.destination, color=palette_a[7], size=10)
        self.files = ft.ListView(padding=0,spacing=0)
        #self.edit_source_label = ft.Container(self.files, bgcolor=palette_a[4], border_radius=2)
        self.edit_destination_label = ft.TextField(value=self.destination, color=palette_a[4], text_size=10, height=15,border_width=0, border_radius=2, content_padding=0)
        self.s_folder_bt = ft.Container(ft.Row([ft.Icon(ft.icons.INSERT_DRIVE_FILE, size=14, color="#1f7fce")]), on_hover=self.bt_hover_a, on_click=select_file)
        self.d_folder_bt = ft.Container(ft.Row([ft.Icon(ft.icons.FOLDER, size=14, color="#01a26d")]), on_hover=self.bt_hover_a, on_click=select_directory)
        self.del_bt = ft.Container(ft.Row([ft.Icon(ft.icons.DELETE, size=14, color=palette_a[4])]), on_click=self.self_remove, visible=False, on_hover=self.bt_hover_a)
        self.yes_bt = ft.Container(ft.Row([ft.Icon(ft.icons.CHECK, size=14, color=palette_a[2])]), on_click=self.edit_yes, visible=False, on_hover=self.bt_hover_a)
        self.cancel_bt = ft.Container(ft.Row([ft.Icon(ft.icons.CLOSE, size=14, color=palette_a[3])]), on_click=self.edit_cancel, visible=False, on_hover=self.bt_hover_a)
        self.path_icon_col = ft.Column([self.s_folder_bt, self.d_folder_bt], spacing=0)
        edit_icon_row = ft.Row([self.yes_bt, self.cancel_bt, self.del_bt], animate_size=ft.animation.Animation(200, ft.AnimationCurve.BOUNCE_OUT))
        
        self.mode_switcher_row = ft.Row([ft.Text("Mode", size=10, color=palette_a[4]), ft.Container(width=15,height=10, bgcolor="#01a26d", border_radius=10), ft.Text("Mode", size=10, color=palette_a[4])], spacing=5, animate_size=ft.animation.Animation(200, ft.AnimationCurve.BOUNCE_OUT))
        self.mode_switcher_con = ft.Container(self.mode_switcher_row, width=60, height=20, bgcolor=palette_a[1], visible=False, border_radius=10, padding=ft.padding.only(left=5, right=5), on_click=self.mode_switcher)
        edit_icon_col = ft.Column([edit_icon_row, self.mode_switcher_con],spacing=2)
        self.view_path_col = ft.Column(controls=[self.source_label, self.destination_label], spacing=0)
        self.edit_path_col = ft.Column(controls=[self.files, self.edit_destination_label], spacing=0, visible=False, expand=True)
        path_col  = ft.Row([self.view_path_col, self.edit_path_col])
        path_row = ft.Row([self.path_icon_col, ft.Container(path_col, on_click=self.edit, expand=True), ft.Container(edit_icon_col, margin=5,)], spacing=3)
        self.path_con = ft.Container(path_row, bgcolor="transparent", expand=True, border_radius=bd_radius, padding=ft.padding.only(left=5, top=2, right=5, bottom=2), border=ft.border.all(1, "#DDE6ED"))
        row = ft.Row(controls=[self.pull_bt, self.path_con, self.push_bt], spacing=5)
        if self.mode == "pull":
            self.push_bt.disabled = True
            self.s_folder_bt.content.controls[0].color="#01a26d"
            self.d_folder_bt.content.controls[0].color="#1f7fce"
            self.mode_switcher_row.controls[0].visible = False
            self.mode_switcher_row.controls[1].bgcolor = "#1f7fce"
            self.mode_switcher_row.controls[2].visible = True
        else:
            self.pull_bt.disabled = True
            self.s_folder_bt.content.controls[0].color="#1f7fce"
            self.d_folder_bt.content.controls[0].color="#01a26d"
            self.mode_switcher_row.controls[0].visible = True
            self.mode_switcher_row.controls[1].bgcolor = "#01a26d"
            self.mode_switcher_row.controls[2].visible = False
        return row
    
    def bt_hover_a(self, e):
        e.control.scale = 1.2 if e.control.scale == 1 else 1
        e.control.update()

    def mode_switcher(self, e):
        if self.mode == "pull":
            self.pull_bt.disabled = True
            self.push_bt.disabled = False
            self.s_folder_bt.content.controls[0].color="#1f7fce"
            self.d_folder_bt.content.controls[0].color="#01a26d"
            self.mode_switcher_row.controls[0].visible = True
            self.mode_switcher_row.controls[1].bgcolor = "#01a26d"
            self.mode_switcher_row.controls[2].visible = False
            self.mode = "push"
        elif self.mode == "push":
            self.pull_bt.disabled = False
            self.push_bt.disabled = True
            self.s_folder_bt.content.controls[0].color="#01a26d"
            self.d_folder_bt.content.controls[0].color="#1f7fce"
            self.mode_switcher_row.controls[0].visible = False
            self.mode_switcher_row.controls[1].bgcolor = "#1f7fce"
            self.mode_switcher_row.controls[2].visible = True
            self.mode = "pull"
        self.update()


    def request(self, e):
        if e.control.text == "PULL":
            self.mode = e.control.text = "PULL"
            for file in self.source:
                copy_file(file, self.destination)
                #page_overlay(f"{file} to {self.destination}", "message")
        elif e.control.text == "PUSH":
            self.mode = e.control.text = "PUSH"
            for file in self.source:
                copy_file(file, self.destination)
                #page_overlay(f"{file} to {self.destination}", "message")
        
    def self_remove(self, e):
        del task_data["command"][self.id]
        self.remove_command(self, self.id)

    def render_files(self):
        self.files.controls.clear()
        del self.path_icon_col.controls[1:-1]
        for i in range(len(self.source)):
                self.files.controls.append(ft.Text(value=self.source[i], color=palette_a[4], size=10, no_wrap=True))
                if i > 0:
                    icon = ft.Container(ft.Row([ft.Icon(ft.icons.INSERT_DRIVE_FILE, size=14, color="transparent")]))
                    self.path_icon_col.controls.insert(1, icon)
        self.update()

    def edit(self, e):
        if self.edit_path_col.visible == False:
            self.view_path_col.visible = False
            self.edit_path_col.visible = True
            self.yes_bt.visible = True
            self.cancel_bt.visible = True
            self.del_bt.visible = True
            self.mode_switcher_con.visible = True
            self.edit_destination_label.value = self.destination_label.value
            self.render_files()
            self.path_con.bgcolor = palette_a[6]
            self.update()
            print("Command Edit")
    
    def edit_yes(self, e):
        self.view_path_col.visible = True
        self.edit_path_col.visible = False
        self.yes_bt.visible = False
        self.cancel_bt.visible = False
        self.del_bt.visible = False
        self.mode_switcher_con.visible = False
        self.path_con.bgcolor = "transparent"
        del self.path_icon_col.controls[1:-1]
        self.source_label.value = str(self.source)
        self.destination_label.value = self.destination
        self.update()
        task_data["command"][self.id]["mode"] = self.mode
        task_data["command"][self.id]["source"] = self.source
        task_data["command"][self.id]["destination"] = self.destination
        saveJsonFile(task_data, "task_data", resource_path("assets/resources"))
        page_overlay("Save", "message")
        print("Save")
    
    def edit_cancel(self, e):
        self.view_path_col.visible = True
        self.edit_path_col.visible = False
        self.yes_bt.visible = False
        self.cancel_bt.visible = False
        self.del_bt.visible = False
        self.mode_switcher_con.visible = False
        self.path_con.bgcolor = "transparent"
        del self.path_icon_col.controls[1:-1]
        self.source = task_data["command"][self.id]["source"]
        self.source_label.value = str(self.source)
        self.update()
        print("Cancel")

class Task(ft.UserControl):
    def __init__(self, id, name, tag, commnd, remove_task):
        super().__init__()
        self.id = id
        self.name = name
        self.tag = tag
        self.commnd = commnd
        self.remove_task = remove_task

    def build(self):
        self.task_name = ft.Text(value=self.name, color=palette_a[7], size=14, no_wrap=True)
        self.edit_task_name = ft.TextField(value=self.name, color=ft.colors.WHITE, text_size=14, height=38, content_padding=ft.padding.only(left=10), bgcolor=palette_a[6], border_width=0)
        self.task_name_con = ft.Container(self.task_name, on_click=self.expand_command_list, expand=True)
        self.yes_bt = ft.IconButton(icon=ft.icons.CHECK, on_click=self.edit_yes, scale=bt_icon_sacle_a, icon_color=palette_a[2], visible=False)
        self.no_bt = ft.IconButton(icon=ft.icons.CLOSE, on_click=self.edit_no, scale=bt_icon_sacle_a, icon_color=palette_a[3], visible=False)
        self.edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=self.edit_task, scale=bt_icon_sacle_a, icon_color=palette_a[7])
        edit_row = ft.Row([self.yes_bt, self.no_bt, self.edit_button],spacing=0,animate_size=ft.animation.Animation(200, ft.AnimationCurve.BOUNCE_OUT))
        self.del_button = ft.IconButton(icon=ft.icons.DELETE, on_click=self.request_delete, scale=bt_icon_sacle_a, visible=True, icon_color=palette_a[7])
        self.yes_s_button = ft.IconButton(icon=ft.icons.CHECK, on_click=self.del_task, scale=bt_icon_sacle_a, icon_color=palette_a[2], visible=False)
        self.no_s_button = ft.IconButton(icon=ft.icons.CLOSE, on_click=self.cancel_delete, scale=bt_icon_sacle_a, icon_color=palette_a[3], visible=False)
        save_button = ft.IconButton(icon=ft.icons.SAVE, on_click=self.save_task, visible=False)
        cancel_edit_button = ft.IconButton(icon=ft.icons.CANCEL, on_click=self.cancel_edit_task, visible=False)
        color_tag = ft.Container(bgcolor=self.tag, width=10, height=40, border_radius=bd_radius)
        delete_row = ft.Row(controls=[self.del_button, self.yes_s_button, self.no_s_button],spacing=0,animate_size=ft.animation.Animation(200, ft.AnimationCurve.BOUNCE_OUT))
        title_row = ft.Row(controls=[self.task_name_con, self.yes_bt, self.no_bt, edit_row, delete_row, save_button, cancel_edit_button])
        command_list_label = ft.Text(value="Commands : ", color="#43474e", size=12, no_wrap=True)
        folder_bt = ft.Container(ft.Row([ft.Icon(ft.icons.FOLDER, size=15, color=palette_a[7]), ft.Icon(ft.icons.ARROW_FORWARD_SHARP, size=15, color=palette_a[7]), ft.Icon(ft.icons.FOLDER, size=15, color=palette_a[7])], spacing=1), tooltip="Folder to Folder",data="DTD", on_hover=self.bt_hover_a, on_click=self.add_command, animate_scale=ft.animation.Animation(300, ft.AnimationCurve.BOUNCE_OUT))
        files_bt = ft.Container(ft.Row([ft.Icon(ft.icons.INSERT_DRIVE_FILE, size=15, color=palette_a[7]), ft.Icon(ft.icons.ARROW_FORWARD_SHARP, size=15, color=palette_a[7]), ft.Icon(ft.icons.FOLDER, size=15, color=palette_a[7])], spacing=1), tooltip="Files to Folder",data="FTD", on_hover=self.bt_hover_a, on_click=self.add_command, animate_scale=ft.animation.Animation(300, ft.AnimationCurve.BOUNCE_OUT))
        self.command_col = ft.Column(controls=[ft.Row([command_list_label, ft.Row([folder_bt, files_bt],spacing=10)])])
        self.command_con = ft.Row(controls=[ft.Container(content=self.command_col, bgcolor="#bdccd6", padding=5, border_radius=bd_radius, expand=True)], visible=False)
        content_col = ft.Column(controls=[title_row], expand=True)
        task_row = ft.Row(controls=[color_tag, content_col])
        task_col = ft.Column(controls=[task_row, self.command_con], spacing=5)
        task = ft.Row(controls=[
                ft.Container(content=task_col, bgcolor="#DDE6ED", padding=5, border_radius=bd_radius, expand=True)]
                ,alignment=ft.MainAxisAlignment.CENTER
                )
        return task
    
    def bt_hover_a(self, e):
        e.control.scale = 1 if e.control.scale == 1.2 else 1.2
        e.control.update()

    def edit_task(self, e):
        self.task_name_con.content = self.edit_task_name
        self.edit_task_name.value = self.task_name.value
        self.edit_button.visible = False
        self.yes_bt.visible = True
        self.no_bt.visible = True
        self.update()
        print("Edit Task")
    
    def edit_yes(self, e):
        self.task_name_con.content = self.task_name
        self.task_name.value = self.edit_task_name.value
        self.edit_button.visible = True
        self.yes_bt.visible = False
        self.no_bt.visible = False
        self.update()
        self.name = self.task_name.value
        task_data["task"][self.id]["name"] = self.name
        saveJsonFile(task_data, "task_data", resource_path("assets/resources"))
        print("Save")
        page_overlay("Save", "message")


    def edit_no(self, e):
        self.task_name_con.content = self.task_name
        self.edit_button.visible = True
        self.yes_bt.visible = False
        self.no_bt.visible = False
        self.update()
        print("Cancel")
    
    def del_task(self, e):
        self.del_button.visible = True
        self.yes_s_button.visible = False
        self.no_s_button.visible = False
        del task_data["task"][self.id]
        self.remove_task(self)
        print(f"Task ID: {self.id} has been deleted!")
        for command in self.commnd:
            del task_data["command"][command]
            print(f"Command ID: {command} has been deleted!")
        #self.update()

    def save_task(self, e):
        saveJsonFile(task_data, "task_data", resource_path("assets/resources"))
        page_overlay("Save", "message")
        print("Save Task")
    
    def cancel_edit_task(self, e):
        print("Cancel Edit Task")

    def request_delete(self, e):
        self.del_button.visible = False
        self.yes_s_button.visible = True
        self.no_s_button.visible = True
        self.update()
        print("Request")

    def cancel_delete(self, e):
        self.del_button.visible = True
        self.yes_s_button.visible = False
        self.no_s_button.visible = False
        self.update()
        print("Cancel Delete")

    def expand_command_list(self, e):
        if self.task_name_con.content == self.task_name:
            if self.command_con.visible == False:
                self.command_con.visible = True
                self.command_render()
                print("Expand Panel Commands")
            elif self.command_con.visible == True:
                self.command_con.visible = False
                print("Close Panel Commands")
        
        self.update()

    def command_render(self):
        del self.command_col.controls[1:]
        for command in self.commnd:
            if "DTD_" in command:
                self.command_col.controls.append(Command_DTD(command, task_data["command"][command]["source"], task_data["command"][command]["destination"], self.remove_command))
            elif "FTD_" in command:
                self.command_col.controls.append(Command_FTD(command, task_data["command"][command]["mode"], task_data["command"][command]["source"], task_data["command"][command]["destination"], self.remove_command))

    def add_command(self, e):
        if e.control.data == "DTD":
            new_id = id_generator("DTD")
            new_command = {new_id:{"source":"D:/", "destination":"C:/"}}
            task_data["command"].update(new_command)
            task_data["task"][self.id]["command"].append(new_id)
            print(f"Command ID: {new_id} " + str(task_data["command"][new_id]))
        elif e.control.data == "FTD":
            new_id = id_generator("FTD")
            new_command = {new_id:{"mode":"push", "source":["Select file"], "destination":"C:/"}}
            task_data["command"].update(new_command)
            task_data["task"][self.id]["command"].append(new_id)
            print(f"Command ID: {new_id} " + str(task_data["command"][new_id]))
        print(task_data["task"][self.id]["command"])
        self.command_render()
        self.update()
        saveJsonFile(task_data, "task_data", resource_path("assets/resources"))
        page_overlay(f"Command added : {new_id}", "message")

    def remove_command(self, command, com_id):
        task_data["task"][self.id]["command"].remove(com_id)
        self.command_col.controls.remove(command)
        self.update()
        saveJsonFile(task_data, "task_data", resource_path("assets/resources"))
        print("Remove Command: " + com_id)
    
class TaskView(ft.UserControl):
    def build(self):
        self.tasks = ft.Column(spacing=6)
        self.view = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(controls=[
                    ft.ElevatedButton(icon=ft.icons.ADD,  text="ADD", bgcolor=palette_a[6], color="#F1F6F9", 
                        style=bt_style_a, 
                        on_hover=self.bt_hover_a,
                        on_click=self.add_task,
                        height=30,
                        scale=1,
                        animate_scale=ft.animation.Animation(300, ft.AnimationCurve.BOUNCE_OUT))
                ],alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=self.tasks,
                    bgcolor="#9DB2BF",
                    padding=6,
                    margin=6,
                    border_radius=bd_radius,
                    animate_size=ft.animation.Animation(150, ft.AnimationCurve.BOUNCE_OUT)
                )
            ],spacing=0
        )
        self.task_render()
        return self.view
    
    def bt_hover_a(self, e):
        e.control.scale = 1.1 if e.control.scale == 1 else 1
        e.control.bgcolor = "#FF8400" if e.data == "true" else palette_a[6]
        e.control.update()
    
    def task_render(self):
        self.tasks.controls.clear()
        for task in task_data["task"]:
            self.tasks.controls.append(Task(task, task_data["task"][task]["name"], task_data["task"][task]["tag"], task_data["task"][task]["command"], self.remove_task))
        print("Render Task")
        
    def add_task(self, e):
        self.tasks.controls.clear()
        new_id = id_generator("TID")
        new_task = {new_id:{"name":"New Task", "tag":palette_b[random.randint(0, len(palette_b)-1)], "command":[]}}
        task_data["task"].update(new_task)
        print("Add Task")
        print("==============Tasks==============")
        for task_id, task_info in task_data["task"].items():
            task_name = task_info["name"]
            print(f"Task ID: {task_id}, Name: {task_name}")
        print("=================================")
        self.task_render()
        self.update()
        saveJsonFile(task_data, "task_data", resource_path("assets/resources"))
        page_overlay(f"Task added : {new_id}", "message")

    def remove_task(self, task):
        self.tasks.controls.remove(task)
        self.update()
        saveJsonFile(task_data, "task_data", resource_path("assets/resources"))
        print("Remove Task")
        page_overlay("Task Removed", "message")

def main(page: ft.Page):
    page.title = "DuckxCopy"
    page.window_width = 600
    page.window_height = 680
    page.padding = 0
    page.bgcolor = palette_a[1]
    # page.horizontal_alignment = "center"
    # page.vertical_alignment = "center"
    page.scroll = "adaptive"
    page.fonts = {"Noto Sans Medium": resource_path("assets/fonts/NotoSans-Medium.ttf")}
    page.theme = ft.Theme(font_family="Noto Sans Medium")

    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True

    page.snack_bar = ft.SnackBar(content=ft.Text("Hello, world!"), action="Alright!")
    title = ft.Row(
            [
                ft.WindowDragArea(ft.Container(ft.Text(""), bgcolor=ft.colors.with_opacity, padding=10), expand=True),
                ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window_close(), icon_color="#F8985C", bgcolor=page.bgcolor)
            ]
        )
    
    text_ovelay = ft.Text(size=12, color="#ffffff")
    footer_icon = ft.Icon(ft.icons.WARNING_ROUNDED, color="#ffffff", size=15)
    #footer = ft.Container(ft.Row([footer_icon, text_ovelay]), width=page.window_width, bgcolor=palette_a[0], bottom=0, padding=ft.padding.only(left=10, top=5, right=5, bottom=5), animate_opacity=ft.animation.Animation(1000, ft.AnimationCurve.FAST_LINEAR_TO_SLOW_EASE_IN), opacity=0)
    page.overlay.extend([title])
    
    global page_overlay
    def page_overlay(text, mode):
        if mode == "alert":
            bgcolor = palette_a[3]
            footer_icon.name = ft.icons.WARNING_ROUNDED
        elif mode == "message":
            bgcolor = palette_a[2]
            footer_icon.name = ft.icons.MESSAGE_ROUNDED
        else:
            text = "Overlay error"
            bgcolor = palette_a[3]
            footer_icon.name = ft.icons.WARNING_ROUNDED
        text_ovelay.value = text
        page.snack_bar = ft.SnackBar(ft.Row([footer_icon, text_ovelay]), bgcolor=bgcolor)
        page.snack_bar.open = True
        page.update()


    def space():
        space = ft.Text(value=" ", color="#9BA4B5", size=5)
        row = ft.Row(controls=[space],alignment=ft.MainAxisAlignment.CENTER)
        page.add(row)
    
    

    space()
    space()

    headerLogo = ft. Image(src=resource_path("assets/resources/imgs/Duckx_logo_light_256.png"), height=48)
    t = ft.Text(value="BATCH COPY", color="#F8985C", size=12)
    c = ft.Container(content=t, bgcolor=page.bgcolor, width=100, border_radius=100, padding=5, alignment=ft.alignment.center)
    c = ft.Container(content=c ,bgcolor=ft.colors.WHITE, padding=1, border_radius=100)
    row = ft.Row(controls=[headerLogo, c],alignment=ft.MainAxisAlignment.CENTER)
    page.add(row)

    space()
    content = ft.Column([TaskView()])
    page.add(content)

if __name__ == '__main__':
    ft.app(main)