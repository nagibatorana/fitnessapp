from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel,
                             QDialog, QFormLayout, QHBoxLayout, QComboBox, QStackedWidget,
                             QTextEdit, QListWidget, QListWidgetItem, QScrollArea, QFrame, QTabWidget, QLabel,
                             QInputDialog, QMessageBox, QSpinBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPalette
import sys

APP_STYLE = """
    QWidget {
        background-color: #1e1e1e;
        color: #ffffff;
        font-family: Arial;
    }

    QPushButton {
        background-color: #700018;
        color: white;
        border: 1px solid #444;
        padding: 8px;
        min-width: 100px;
        border-radius: 4px;
    }

    QPushButton:hover {
        background-color: #900020;
    }

    QPushButton:pressed {
        background-color: #500010;
    }

    QLineEdit, QTextEdit, QComboBox, QListWidget {
        background-color: #2a2a2a;
        color: white;
        border: 1px solid #444;
        padding: 5px;
        border-radius: 4px;
    }

    QTabWidget::pane {
        border: 1px solid #444;
        background: #2a2a2a;
    }

    QTabBar::tab {
        background: #2a2a2a;
        color: white;
        padding: 8px;
        border: 1px solid #444;
        border-bottom: none;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }

    QTabBar::tab:selected {
        background: #700018;
        border-color: #444;
    }

    QScrollArea {
        border: none;
    }

    QFrame {
        border: 1px solid #444;
        border-radius: 4px;
    }

    QLabel {
        color: #ffffff;
    }

    QMessageBox {
        background-color: #1e1e1e;
    }

    QMessageBox QLabel {
        color: #ffffff;
    }

    QMessageBox QPushButton {
        min-width: 80px;
    }

    QSpinBox {
        background-color: #2a2a2a;
        color: white;
        border: 1px solid #444;
        padding: 5px;
        border-radius: 4px;
    }
"""


class Exercise:
    def __init__(self, name, description, muscle_group, sets=3, reps=10):
        self.name = name
        self.description = description
        self.muscle_group = muscle_group
        self.sets = sets
        self.reps = reps

class Training:
    def __init__(self, name, is_predefined=False):
        self.name = name
        self.exercises = []
        self.is_predefined = is_predefined

    def add_exercise(self, exercise):
        self.exercises.append(exercise)

    def remove_exercise(self, index):
        if 0 <= index < len(self.exercises):
            self.exercises.pop(index)

class ExerciseSelectionWindow(QDialog):
    exercise_selected = pyqtSignal(Exercise)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор упражнений")
        self.setFixedSize(800, 600)
        self.setStyleSheet(APP_STYLE)

        self.all_exercises = self.load_all_exercises()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        filter_layout = QHBoxLayout()
        self.muscle_group_combo = QComboBox()
        self.muscle_group_combo.addItems(["Все группы", "Грудь", "Спина", "Ноги", "Плечи", "Пресс", "Руки"])
        self.muscle_group_combo.currentIndexChanged.connect(self.filter_exercises)
        filter_layout.addWidget(QLabel("Группа мышц:"))
        filter_layout.addWidget(self.muscle_group_combo)
        layout.addLayout(filter_layout)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск упражнений...")
        self.search_input.textChanged.connect(self.filter_exercises)
        layout.addWidget(self.search_input)
        self.exercise_list = QListWidget()
        self.populate_exercise_list()
        layout.addWidget(self.exercise_list)

        reps_layout = QHBoxLayout()
        reps_layout.addWidget(QLabel("Подходы:"))
        self.sets_spin = QSpinBox()
        self.sets_spin.setRange(1, 10)
        self.sets_spin.setValue(3)
        reps_layout.addWidget(self.sets_spin)
        reps_layout.addWidget(QLabel("Повторения:"))
        self.reps_spin = QSpinBox()
        self.reps_spin.setRange(1, 30)
        self.reps_spin.setValue(10)
        reps_layout.addWidget(self.reps_spin)
        reps_layout.addStretch()
        layout.addLayout(reps_layout)

        buttons_layout = QHBoxLayout()
        select_button = QPushButton("Выбрать")
        select_button.clicked.connect(self.select_exercise)
        buttons_layout.addWidget(select_button)
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        buttons_layout.addWidget(close_button)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
    def load_all_exercises(self):
        return [
            Exercise("Жим штанги лёжа", "Лежа на скамье, опустите штангу до груди, затем выжмите вверх", "Грудь"),
            Exercise("Жим гантелей лежа", "Лежа на скамье, жмите гантели вверх от груди", "Грудь"),
            Exercise("Отжимания на брусьях", "На брусьях, опускайтесь до сгиба локтей под 90 градусов", "Грудь"),
            Exercise("Пуловер с гантелью", "Лежа на скамье, опускайте гантель за голову и поднимайте обратно", "Грудь"),
            Exercise("Сведение рук в кроссовере", "Стоя между стойками, сводите руки перед собой", "Грудь"),
            Exercise("Подтягивания широким хватом", "Подтягивайтесь, держась за перекладину широким хватом", "Спина"),
            Exercise("Тяга штанги в наклоне", "В наклоне, тяните штангу к поясу", "Спина"),
            Exercise("Тяга гантели одной рукой", "С упором на скамью, тяните гантель к поясу", "Спина"),
            Exercise("Гиперэкстензия", "На тренажере, поднимайте корпус, держа спину прямой", "Спина"),
            Exercise("Шраги со штангой", "Стоя, поднимайте плечи, держа штангу в руках", "Спина"),
            Exercise("Приседания со штангой", "Штанга на плечах, приседайте до параллели с полом", "Ноги"),
            Exercise("Жим ногами", "В тренажере, выжимайте платформу ногами", "Ноги"),
            Exercise("Выпады с гантелями", "С гантелями, делайте шаг вперед и опускайтесь", "Ноги"),
            Exercise("Румынская тяга", "Со слегка согнутыми коленями, наклоняйтесь со штангой", "Ноги"),
            Exercise("Подъемы на носки", "Стоя на возвышении, поднимайтесь на носках", "Ноги"),
            Exercise("Жим штанги стоя", "Стоя, выжимайте штангу над головой", "Плечи"),
            Exercise("Махи гантелями в стороны", "Стоя, поднимайте гантели через стороны", "Плечи"),
            Exercise("Тяга штанги к подбородку", "Узким хватом, тяните штангу к подбородку", "Плечи"),
            Exercise("Разведение гантелей в наклоне", "В наклоне, разводите гантели в стороны", "Плечи"),
            Exercise("Жим Арнольда", "Сидя, жмите гантели с вращением", "Плечи"),
            Exercise("Подъем штанги на бицепс", "Стоя, поднимайте штангу на бицепс", "Руки"),
            Exercise("Молотковые сгибания", "С гантелями, поднимайте их нейтральным хватом", "Руки"),
            Exercise("Французский жим лежа", "Лежа, опускайте штангу ко лбу и разгибайте", "Руки"),
            Exercise("Отжимания от скамьи", "С упором сзади, опускайтесь и поднимайтесь", "Руки"),
            Exercise("Разгибание рук на блоке", "На блоке, разгибайте руки вниз", "Руки"),
            Exercise("Скручивания", "Лежа, поднимайте корпус, скручивая пресс", "Пресс"),
            Exercise("Подъем ног в висе", "На перекладине, поднимайте ноги до параллели", "Пресс"),
            Exercise("Планка", "Удерживайте положение на локтях и носках", "Пресс"),
            Exercise("Русские скручивания", "Сидя, поворачивайте корпус с весом", "Пресс"),
            Exercise("Велосипед", "Лежа, имитируйте езду на велосипеде", "Пресс")
        ]

    def populate_exercise_list(self):
        self.exercise_list.clear()
        for exercise in self.all_exercises:
            item = QListWidgetItem(f"{exercise.name} ({exercise.muscle_group})")
            item.setData(Qt.UserRole, exercise)
            self.exercise_list.addItem(item)
    def filter_exercises(self):
        search_text = self.search_input.text().lower()
        muscle_group = self.muscle_group_combo.currentText()
        self.exercise_list.clear()
        for exercise in self.all_exercises:
            matches = True
            if muscle_group != "Все группы" and exercise.muscle_group != muscle_group:
                matches = False
            if search_text and search_text not in exercise.name.lower():
                matches = False
            if matches:
                item = QListWidgetItem(f"{exercise.name} ({exercise.muscle_group})")
                item.setData(Qt.UserRole, exercise)
                self.exercise_list.addItem(item)
    def select_exercise(self):
        selected_items = self.exercise_list.selectedItems()
        if selected_items:
            exercise = selected_items[0].data(Qt.UserRole)
            custom_exercise = Exercise(
                name=exercise.name,
                description=exercise.description,
                muscle_group=exercise.muscle_group,
                sets=self.sets_spin.value(),
                reps=self.reps_spin.value()
            )
            self.exercise_selected.emit(custom_exercise)
            self.close()
class ExerciseDetailsWindow(QDialog):
    def __init__(self, exercise, parent=None):
        super().__init__(parent)
        self.setWindowTitle(exercise.name)
        self.setFixedSize(500, 400)
        self.setStyleSheet(APP_STYLE)
        layout = QVBoxLayout()
        title_label = QLabel(exercise.name)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ff3333;")
        layout.addWidget(title_label)
        group_label = QLabel(f"Группа мышц: {exercise.muscle_group}")
        layout.addWidget(group_label)
        sets_reps_label = QLabel(f"Подходы: {exercise.sets} x Повторения: {exercise.reps}")
        sets_reps_label.setStyleSheet("font-size: 14px; color: #aaaaaa;")
        layout.addWidget(sets_reps_label)
        description_label = QLabel("Описание:\n" + exercise.description)
        description_label.setWordWrap(True)
        layout.addWidget(description_label)
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)
class TrainingDetailsWindow(QDialog):
    def __init__(self, training, parent=None):
        super().__init__(parent)
        self.setWindowTitle(training.name)
        self.setFixedSize(700, 600)
        self.setStyleSheet(APP_STYLE)
        self.training = training
        layout = QVBoxLayout()
        self.exercise_list = QListWidget()
        self.exercise_list.itemDoubleClicked.connect(self.view_exercise_details)
        self.populate_exercise_list()
        layout.addWidget(self.exercise_list)
        buttons_layout = QHBoxLayout()
        if not training.is_predefined:
            add_button = QPushButton("Добавить упражнение")
            add_button.clicked.connect(self.add_exercise)
            buttons_layout.addWidget(add_button)
            remove_button = QPushButton("Удалить упражнение")
            remove_button.clicked.connect(self.remove_exercise)
            buttons_layout.addWidget(remove_button)
        edit_button = QPushButton("Изменить подходы/повторения")
        edit_button.clicked.connect(self.edit_sets_reps)
        buttons_layout.addWidget(edit_button)
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.accept)
        buttons_layout.addWidget(close_button)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
    def populate_exercise_list(self):
        self.exercise_list.clear()
        for exercise in self.training.exercises:
            item = QListWidgetItem(f"{exercise.name} ({exercise.muscle_group}) - {exercise.sets} x {exercise.reps}")
            item.setData(Qt.UserRole, exercise)
            self.exercise_list.addItem(item)
    def view_exercise_details(self, item):
        exercise = item.data(Qt.UserRole)
        details_window = ExerciseDetailsWindow(exercise, self)
        details_window.exec_()
    def add_exercise(self):
        selection_dialog = ExerciseSelectionWindow(self)
        selection_dialog.exercise_selected.connect(self.handle_exercise_selected)
        selection_dialog.exec_()
    def handle_exercise_selected(self, exercise):
        self.training.add_exercise(exercise)
        self.populate_exercise_list()

    def remove_exercise(self):
        selected_items = self.exercise_list.selectedItems()
        if selected_items:
            row = self.exercise_list.row(selected_items[0])
            self.training.remove_exercise(row)
            self.populate_exercise_list()

    def edit_sets_reps(self):
        selected_items = self.exercise_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Ошибка", "Выберите упражнение для изменения")
            return
        row = self.exercise_list.row(selected_items[0])
        exercise = self.training.exercises[row]
        dialog = QDialog(self)
        dialog.setWindowTitle("Изменение подходов и повторений")
        dialog.setFixedSize(300, 200)
        dialog.setStyleSheet(APP_STYLE)
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        sets_spin = QSpinBox()
        sets_spin.setRange(1, 10)
        sets_spin.setValue(exercise.sets)
        form_layout.addRow("Подходы:", sets_spin)
        reps_spin = QSpinBox()
        reps_spin.setRange(1, 30)
        reps_spin.setValue(exercise.reps)
        form_layout.addRow("Повторения:", reps_spin)
        layout.addLayout(form_layout)
        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(lambda: self.save_sets_reps(exercise, sets_spin.value(), reps_spin.value(), dialog))
        buttons_layout.addWidget(save_button)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(dialog.reject)
        buttons_layout.addWidget(cancel_button)
        layout.addLayout(buttons_layout)
        dialog.setLayout(layout)
        dialog.exec_()
    def save_sets_reps(self, exercise, sets, reps, dialog):
        exercise.sets = sets
        exercise.reps = reps
        self.populate_exercise_list()
        dialog.accept()

class CreateTrainingWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Создать тренировку")
        self.setFixedSize(700, 600)
        self.setStyleSheet(APP_STYLE)
        layout = QVBoxLayout()
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Название тренировки:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название тренировки")
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        self.exercise_list = QListWidget()
        self.exercise_list.itemDoubleClicked.connect(self.view_exercise_details)
        layout.addWidget(self.exercise_list)
        buttons_layout = QHBoxLayout()
        add_button = QPushButton("Добавить упражнение")
        add_button.clicked.connect(self.add_exercise)
        buttons_layout.addWidget(add_button)
        remove_button = QPushButton("Удалить упражнение")
        remove_button.clicked.connect(self.remove_exercise)
        buttons_layout.addWidget(remove_button)
        layout.addLayout(buttons_layout)
        save_buttons_layout = QHBoxLayout()
        save_button = QPushButton("Сохранить тренировку")
        save_button.clicked.connect(self.save_training)
        save_buttons_layout.addWidget(save_button)
        done_button = QPushButton("Готово")
        done_button.clicked.connect(self.finish_editing)
        save_buttons_layout.addWidget(done_button)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        save_buttons_layout.addWidget(cancel_button)
        layout.addLayout(save_buttons_layout)
        self.setLayout(layout)
        self.training = Training("Новая тренировка")

    def view_exercise_details(self, item):
        exercise = item.data(Qt.UserRole)
        details_window = ExerciseDetailsWindow(exercise, self)
        details_window.exec_()
    def add_exercise(self):
        selection_dialog = ExerciseSelectionWindow(self)
        selection_dialog.exercise_selected.connect(self.handle_exercise_selected)
        selection_dialog.exec_()
    def handle_exercise_selected(self, exercise):
        self.training.add_exercise(exercise)
        self.update_exercise_list()

    def remove_exercise(self):
        selected_items = self.exercise_list.selectedItems()
        if selected_items:
            row = self.exercise_list.row(selected_items[0])
            self.training.remove_exercise(row)
            self.update_exercise_list()

    def update_exercise_list(self):
        self.exercise_list.clear()
        for exercise in self.training.exercises:
            item = QListWidgetItem(f"{exercise.name} ({exercise.muscle_group}) - {exercise.sets} x {exercise.reps}")
            item.setData(Qt.UserRole, exercise)
            self.exercise_list.addItem(item)

    def save_training(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название тренировки")
            return
        if not self.training.exercises:
            QMessageBox.warning(self, "Ошибка", "Добавьте хотя бы одно упражнение")
            return
        self.training.name = name
        QMessageBox.information(self, "Сохранено", "Тренировка успешно сохранена!")

    def finish_editing(self):
        if not self.training.name.strip():
            self.training.name = "Без названия"
        if not self.training.exercises:
            reply = QMessageBox.question(
                self, "Пустая тренировка",
                "В тренировке нет упражнений. Все равно сохранить?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        self.accept()


class TrainingWidget(QFrame):
    def __init__(self, training, parent=None):
        super().__init__(parent)
        self.training = training
        self.setFrameShape(QFrame.StyledPanel)
        self.setLineWidth(2)
        self.setStyleSheet("""
            TrainingWidget {
                background-color: #2a2a2a;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
                border: 1px solid #444;
            }
            TrainingWidget[selected=true] {
                background-color: #700018;
                border: 2px solid #900020;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #700018;
                color: white;
                border: 1px solid #444;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #900020;
            }
        """)
        self.selected = False
        layout = QVBoxLayout()
        title_label = QLabel(training.name)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ff3333;")
        layout.addWidget(title_label)
        exercises_label = QLabel(f"Упражнений: {len(training.exercises)}")
        layout.addWidget(exercises_label)
        muscle_groups = ", ".join(sorted({ex.muscle_group for ex in training.exercises}))
        groups_label = QLabel(f"Группы мышц: {muscle_groups}")
        groups_label.setWordWrap(True)
        layout.addWidget(groups_label)
        self.view_button = QPushButton("Просмотреть")
        self.view_button.clicked.connect(self.view_training)
        layout.addWidget(self.view_button)
        self.setLayout(layout)
    def view_training(self):
        details_window = TrainingDetailsWindow(self.training, self)
        details_window.exec_()
    def set_selected(self, selected):
        self.selected = selected
        self.setProperty("selected", selected)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
    def mousePressEvent(self, event):
        if self.selected:
            self.set_selected(False)
            if self.parent() and hasattr(self.parent(), 'select_training'):
                self.parent().select_training(None)
        else:
            self.set_selected(True)
            if self.parent() and hasattr(self.parent(), 'select_training'):
                self.parent().select_training(self)
        super().mousePressEvent(event)

class TrainingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Тренировки")
        self.setFixedSize(900, 700)
        self.setStyleSheet(APP_STYLE)
        self.current_selected_widget = None
        self.trainings = []
        self.load_trainings()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.trainings_scroll = QScrollArea()
        self.trainings_scroll.setWidgetResizable(True)
        self.trainings_container = QWidget()
        self.trainings_layout = QVBoxLayout()
        self.trainings_layout.setAlignment(Qt.AlignTop)
        self.trainings_container.setLayout(self.trainings_layout)
        self.trainings_scroll.setWidget(self.trainings_container)
        layout.addWidget(self.trainings_scroll)
        buttons_layout = QHBoxLayout()
        create_button = QPushButton("Создать свою тренировку")
        create_button.clicked.connect(self.create_training)
        buttons_layout.addWidget(create_button)
        edit_button = QPushButton("Изменить тренировку")
        edit_button.clicked.connect(self.edit_training)
        buttons_layout.addWidget(edit_button)
        delete_button = QPushButton("Удалить тренировку")
        delete_button.clicked.connect(self.delete_training)
        buttons_layout.addWidget(delete_button)
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        buttons_layout.addWidget(close_button)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        self.update_trainings_list()

    def load_trainings(self):
        self.trainings = []
        shoulders_arms = Training("Плечи + Руки", is_predefined=True)
        shoulders_arms.add_exercise(Exercise("Жим штанги стоя", "Стоя, выжимайте штангу над головой", "Плечи", 4, 8))
        shoulders_arms.add_exercise(Exercise("Жим гантелей сидя", "Сидя, жмите гантели вверх", "Плечи", 4, 10))
        shoulders_arms.add_exercise(
            Exercise("Подъем гантелей в стороны", "Стоя, поднимайте гантели через стороны", "Плечи", 3, 12))
        shoulders_arms.add_exercise(
            Exercise("Тяга штанги к подбородку", "Узким хватом, тяните штангу к подбородку", "Плечи", 3, 10))
        shoulders_arms.add_exercise(
            Exercise("Подъем штанги на бицепс", "Стоя, поднимайте штангу на бицепс", "Руки", 4, 8))
        shoulders_arms.add_exercise(
            Exercise("Молотковые сгибания", "С гантелями, поднимайте их нейтральным хватом", "Руки", 3, 10))
        shoulders_arms.add_exercise(
            Exercise("Французский жим лежа", "Лежа, опускайте штангу ко лбу и разгибайте", "Руки", 3, 8))
        self.trainings.append(shoulders_arms)
        
        chest_back = Training("Грудь + Спина", is_predefined=True)
        chest_back.add_exercise(
            Exercise("Жим штанги лёжа", "Лежа на скамье, опустите штангу до груди, затем выжмите вверх", "Грудь", 4, 6))
        chest_back.add_exercise(
            Exercise("Жим гантелей на наклонной скамье", "На наклонной скамье, жмите гантели вверх", "Грудь", 4, 8))
        chest_back.add_exercise(
            Exercise("Разведение гантелей лежа", "Лежа, разводите гантели в стороны", "Грудь", 3, 12))
        chest_back.add_exercise(
            Exercise("Подтягивания широким хватом", "Подтягивайтесь, держась за перекладину широким хватом", "Спина", 4,
                     8))
        chest_back.add_exercise(Exercise("Тяга штанги в наклоне", "В наклоне, тяните штангу к поясу", "Спина", 4, 8))
        chest_back.add_exercise(Exercise("Тяга горизонтального блока", "Сидя, тяните рукоять к поясу", "Спина", 4, 10))
        chest_back.add_exercise(
            Exercise("Гиперэкстензия", "На тренажере, поднимайте корпус, держа спину прямой", "Спина", 3, 12))
        self.trainings.append(chest_back)

        legs_abs = Training("Ноги + Пресс", is_predefined=True)
        legs_abs.add_exercise(
            Exercise("Приседания со штангой", "Штанга на плечах, приседайте до параллели с полом", "Ноги", 4, 6))
        legs_abs.add_exercise(Exercise("Жим ногами", "В тренажере, выжимайте платформу ногами", "Ноги", 4, 8))
        legs_abs.add_exercise(
            Exercise("Румынская тяга", "Со слегка согнутыми коленями, наклоняйтесь со штангой", "Ноги", 4, 8))
        legs_abs.add_exercise(
            Exercise("Выпады с гантелями", "С гантелями, делайте шаг вперед и опускайтесь", "Ноги", 3, 10))
        legs_abs.add_exercise(
            Exercise("Подъем ног в висе", "На перекладине, поднимайте ноги до параллели", "Пресс", 3, 10))
        legs_abs.add_exercise(
            Exercise("Скручивания на наклонной скамье", "На наклонной скамье, поднимайте корпус", "Пресс", 3, 15))
        self.trainings.append(legs_abs)

        fullbody = Training("Фулбади", is_predefined=True)
        fullbody.add_exercise(
            Exercise("Становая тяга", "Стоя, поднимайте штангу с пола, держа спину прямой", "Спина", 4, 6))
        fullbody.add_exercise(Exercise("Жим штанги стоя", "Стоя, выжимайте штангу над головой", "Плечи", 4, 8))
        fullbody.add_exercise(
            Exercise("Отжимания на брусьях", "На брусьях, опускайтесь до сгиба локтей под 90 градусов", "Грудь", 3, 10))
        fullbody.add_exercise(
            Exercise("Приседания с гантелями", "С гантелями, приседайте до параллели с полом", "Ноги", 4, 10))
        fullbody.add_exercise(Exercise("Планка", "Удерживайте положение на локтях и носках", "Пресс", 3, 60))
        self.trainings.append(fullbody)

    def update_trainings_list(self):
        for i in reversed(range(self.trainings_layout.count())):
            self.trainings_layout.itemAt(i).widget().setParent(None)
        for training in self.trainings:
            widget = TrainingWidget(training, self)
            self.trainings_layout.addWidget(widget)

    def create_training(self):
        create_dialog = CreateTrainingWindow(self)
        if create_dialog.exec_() == QDialog.Accepted and create_dialog.training.exercises:
            self.trainings.append(create_dialog.training)
            self.update_trainings_list()
            QMessageBox.information(self, "Успех", "Тренировка успешно создана!")

    def edit_training(self):
        selected_index = self.get_selected_training_index()
        if selected_index is not None:
            training = self.trainings[selected_index]
            if training.is_predefined:
                QMessageBox.warning(self, "Ошибка", "Нельзя изменять предопределенные тренировки")
                return
            edit_dialog = CreateTrainingWindow(self)
            edit_dialog.training = training
            edit_dialog.name_input.setText(training.name)
            edit_dialog.update_exercise_list()
            if edit_dialog.exec_() == QDialog.Accepted:
                self.update_trainings_list()
                QMessageBox.information(self, "Успех", "Тренировка успешно изменена!")

    def delete_training(self):
        selected_index = self.get_selected_training_index()
        if selected_index is not None:
            training = self.trainings[selected_index]
            if training.is_predefined:
                QMessageBox.warning(self, "Ошибка", "Нельзя удалять предопределенные тренировки")
                return
            reply = QMessageBox.question(
                self, 'Удаление тренировки',
                f'Вы уверены, что хотите удалить тренировку "{training.name}"?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.trainings.pop(selected_index)
                self.update_trainings_list()
                QMessageBox.information(self, "Успех", "Тренировка успешно удалена!")

    def get_selected_training_index(self):
        if not self.current_selected_widget:
            QMessageBox.warning(self, "Ошибка", "Выберите тренировку")
            return None
        for i, training in enumerate(self.trainings):
            if training.name == self.current_selected_widget.training.name:
                return i
        return None

    def select_training(self, widget):
        if self.current_selected_widget:
            self.current_selected_widget.set_selected(False)
        self.current_selected_widget = widget
        if widget:
            widget.set_selected(True)

class BjuWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Введите параметры тела")
        self.setFixedSize(800, 600)
        self.setStyleSheet(APP_STYLE)
        self.init_ui()

    def init_ui(self):
        form_layout = QFormLayout()
        self.height_input = QLineEdit(self)
        self.weight_input = QLineEdit(self)
        self.gender_input = QComboBox(self)
        self.gender_input.addItem("Мужчина")
        self.gender_input.addItem("Женщина")
        self.gender_input.setCurrentIndex(1)
        self.age_input = QLineEdit(self)
        form_layout.addRow("Рост (см):", self.height_input)
        form_layout.addRow("Вес (кг):", self.weight_input)
        form_layout.addRow("Пол:", self.gender_input)
        form_layout.addRow("Возраст:", self.age_input)
        self.goal_input = QComboBox(self)
        self.goal_input.addItem("Сушка (снижение веса без потери мышц)")
        self.goal_input.addItem("Обычное похудение (снижение веса вместе с мышцами)")
        self.goal_input.addItem("Поддержание веса")
        self.goal_input.addItem("Набор массы")
        form_layout.addRow("Цель:", self.goal_input)
        self.steps_input = QComboBox(self)
        self.steps_input.addItem("Менее 5000 шагов в день")
        self.steps_input.addItem("5000-10000 шагов в день")
        self.steps_input.addItem("Более 10000 шагов в день")
        form_layout.addRow("Количество шагов:", self.steps_input)
        self.sport_input = QComboBox(self)
        self.sport_input.addItem("Нет занятий спортом")
        self.sport_input.addItem("1-3 тренировки в неделю")
        self.sport_input.addItem("3-5 тренировок в неделю")
        self.sport_input.addItem("Ежедневные тренировки")
        form_layout.addRow("Занятия спортом:", self.sport_input)
        self.work_input = QComboBox(self)
        self.work_input.addItem("Сидячая работа")
        self.work_input.addItem("Работа с легкой активностью")
        self.work_input.addItem("Активная работа")
        self.work_input.addItem("Тяжелая физическая работа")
        form_layout.addRow("Тип работы:", self.work_input)
        buttons_layout = QHBoxLayout()
        submit_button = QPushButton("Подтвердить", self)
        submit_button.clicked.connect(self.submit_parameters)
        buttons_layout.addWidget(submit_button)
        close_button = QPushButton("Закрыть", self)
        close_button.clicked.connect(self.close)
        buttons_layout.addWidget(close_button)
        form_layout.addRow(buttons_layout)

        self.result_label = QLabel(self)
        self.result_label.setWordWrap(True)
        form_layout.addWidget(self.result_label)
        self.water_label = QLabel(self)
        self.water_label.setWordWrap(True)
        form_layout.addWidget(self.water_label)
        self.setLayout(form_layout)

    def calculate_activity_level(self):
        steps_index = self.steps_input.currentIndex()
        sport_index = self.sport_input.currentIndex()
        work_index = self.work_input.currentIndex()
        total_score = steps_index + sport_index + work_index
        if total_score <= 2:
            return 1.2  
        elif total_score <= 5:
            return 1.375  
        elif total_score <= 7:
            return 1.55  
        elif total_score <= 9:
            return 1.7  
        else:
            return 1.9  

    def submit_parameters(self):
        try:
            height = float(self.height_input.text())
            weight = float(self.weight_input.text())
            gender = self.gender_input.currentText()
            age = int(self.age_input.text())
            goal = self.goal_input.currentText()
        except ValueError:
            self.result_label.setText("Пожалуйста, введите корректные данные.")
            return
        activity_multiplier = self.calculate_activity_level()

        if gender == "Мужчина":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        tdee = bmr * activity_multiplier
        if "сушка" in goal.lower():
            min_calories = tdee * 0.85  
            max_calories = tdee * 0.9  
            protein_range = (2.2, 2.5)
            fat_range = (0.8, 1.0)
            ugl_range = (1.5, 2.5)
        elif "обычное похудение" in goal.lower():
            min_calories = tdee * 0.75  
            max_calories = tdee * 0.85  
            protein_range = (1.6, 2.0)
            fat_range = (0.8, 1.0)
            ugl_range = (2, 3)
        elif "поддержание" in goal.lower():
            min_calories = tdee * 0.95  
            max_calories = tdee * 1.05  
            protein_range = (1.4, 1.8)
            fat_range = (1.0, 1.2)
            ugl_range = (3, 4)
        else:  
            min_calories = tdee * 1.1  
            max_calories = tdee * 1.2  
            protein_range = (1.8, 2.2)
            fat_range = (1.0, 1.3)
            ugl_range = (4, 6)

        protein_min = weight * protein_range[0]
        protein_max = weight * protein_range[1]
        fat_min = weight * fat_range[0]
        fat_max = weight * fat_range[1]
        ugl_min = weight * ugl_range[0]
        ugl_max = weight * ugl_range[1]
        base_water = weight * 30  
        activity_level = self.calculate_activity_level()
        if activity_level <= 1.2:
            water_min = base_water
            water_max = base_water * 1.1
        elif activity_level <= 1.375:
            water_min = base_water * 1.1
            water_max = base_water * 1.2
        elif activity_level <= 1.55:
            water_min = base_water * 1.2
            water_max = base_water * 1.3
        elif activity_level <= 1.7:
            water_min = base_water * 1.3
            water_max = base_water * 1.4
        else:
            water_min = base_water * 1.4
            water_max = base_water * 1.5
        if "сушка" in goal.lower() or "похудение" in goal.lower():
            water_min *= 1.1
            water_max *= 1.1

        result_text = (f"<b>Суточная потребность в калориях:</b> {min_calories:.0f} - {max_calories:.0f} ккал<br>"
                       f"<b>Белки:</b> {protein_min:.1f} - {protein_max:.1f} г<br>"
                       f"<b>Жиры:</b> {fat_min:.1f} - {fat_max:.1f} г<br>"
                       f"<b>Углеводы:</b> {ugl_min:.1f} - {ugl_max:.1f} г")
        self.result_label.setText(result_text)
        water_text = (f"<b>Рекомендуемое количество воды:</b> {water_min:.0f}-{water_max:.0f} мл в день<br>"
                      f"(или примерно {water_min / 1000:.1f}-{water_max / 1000:.1f} литров)")
        self.water_label.setText(water_text)

class ReferenceWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Справочная информация")
        self.setFixedSize(800, 600)
        self.setStyleSheet(APP_STYLE)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        sports_nutrition_tab = QWidget()
        sports_layout = QVBoxLayout()
        sports_text = QTextEdit()
        sports_text.setReadOnly(True)
        sports_text.setHtml("""
        <h2 style="color: #ff3333;">Спортивное питание</h2>
        <h3>Протеин</h3>
        <p>Самый востребованный и распространенный вид спортивной добавки. Представляет собой концентрированную, высокобелковую смесь, необходимую для роста мышечной массы. В качестве сырья используются молочные продукты, мясо, бобовые, некоторые растения. Принимается на ежедневной основе как дополнительный источник белка. Время приема: в течение дня, до и после тренировки. Курс приема неограничен.</p>

        <h3>Гейнер</h3>
        <p>Углеводно-белковая смесь. Служит источником калорий и стройматериалом для мышц атлета. Предназначен для набора массы. Используется как альтернатива пропущенному приему пищи или как высококалорийный перекус, а также в качестве послетренировочного восстановителя. Принимается ежедневно вплоть до набора необходимого веса.</p>

        <h3>Аминокислоты</h3>
        <p>Составные части белка, которые выделены в отдельные добавки с калорийностью близкой к нулю. Основа применения - восстановление организма после физической нагрузки и рост сухой мышечной массы. Отдельные аминокислоты играют каждая собственную роль в организме, и прием одних способствует как похудению, так и росту массы, использование других - оздоровлению, третьих - работе мозга и т.д. Комплексные аминки, а также BCAA оптимально принимать до и после, либо во время тренировки. Курс приема неограничен.</p>

        <h3>Жиросжигатели</h3>
        <p>Препараты, стимулирующие снижение веса. Среди средств для похудения выделяют ряд типов по механизму действия, но все они служат одной цели - избавлению от лишних килограммов. Принимаются чаще всего в первой половине дня на ежедневной основе, курсом от месяца до двух.</p>

        <h3>Креатин</h3>
        <p>Вещество, повышающее количество энергии, силу, выносливость, помогает наращивать мышечную массу. Принимается ежедневно по 5-10 гр совместно с быстрыми углеводами (сахар, сок, гейнер), протеином или аминокислотными комплексами. Курс приема: месяц, после чего 2 недели перерыв.</p>

        <h3>Витамино-минеральные комплексы</h3>
        <p>Добавки, предназначенные для восполнения важнейших микроэлементов с целью здоровой работы всего организма. Употреблять каждый день вместе с едой. Курс приема индивидуален. Стандартно: месяц через 2 недели.</p>

        <h3>Л-карнитин</h3>
        <p>Вещество, родственное витаминам и используемое в основном для похудения. Прием в виде добавки позволяет лучше использовать жир в качестве энергии, усиливает жировой метаболизм, способствует укреплению сердечно-сосудистой системы и благоприятно воздействует на иные функции организма. Принимать по 3000-4000 мг перед тренировкой. В дни отдыха по 500 мг 3-4 раза в день за 30-40 мин до приема пищи. Курс: 1,5-2 месяца, затем аналогичный времени приема перерыв.</p>

        <h3>Изотоники и гипотоники</h3>
        <p>Минеральные энергетические напитки с витаминами, солями и, зачастую, углеводами. Восстанавливают водно-солевой баланс организма, нарушаемый при интенсивном потоотделении во время физических нагрузок, ускоряют восстановление, снижают риск травмы и появления судорог. Основная сфера применения - виды спорта с длительной интенсивной нагрузкой: бег, кроссфит, велоспорт и т.д. Принимаются непосредственно во время занятия в качестве напитка или сразу после завершения.</p>

        <h3>Предтренировочные комплексы</h3>
        <p>Добавки, принимаемые перед тренировкой. Это преимущественно стимуляторы для повышения производительности и силы. Принимать на постоянной основе не рекомендуется, делайте перерывы.</p>

        <h3>Тестобустеры</h3>
        <p>Препараты, улучшающие выработку таких гормонов как тестостерон, гормон роста, инсулиноподобный фактор роста и т.д. Принимаются курсами по 1-2 месяца в зависимости от дозировок и типа препарата.</p>

        <h3>Добавки для суставов и связок</h3>
        <p>Вещества, способствующие восстановлению после травм, снятию воспаления, укреплению связочного аппарата. Курс приема не менее 2-3 месяцев, перерыв равен времени приема.</p>
        """)
        sports_layout.addWidget(sports_text)
        sports_nutrition_tab.setLayout(sports_layout)

        periodization_tab = QWidget()
        periodization_layout = QVBoxLayout()
        periodization_text = QTextEdit()
        periodization_text.setReadOnly(True)
        periodization_text.setHtml("""
        <h2 style="color: #ff3333;">Периодизация в спорте</h2>
        <p>Периодизация — это планирование тренировочного процесса, разделенное на отдельные периоды, с целью оптимизации результатов и предотвращения перетренированности. Она учитывает адаптацию организма к нагрузке и позволяет планомерно развивать необходимые физические качества.</p>

        <h3>1. Линейная периодизация (Linear Periodization)</h3>
        <p><b>Описание:</b> Самый простой и классический подход, при котором нагрузка постепенно увеличивается от периода к периоду. Обычно тренировочный цикл делится на три этапа:</p>
        <ul>
            <li><b>Фаза гипертрофии (подготовительная):</b> Основной акцент делается на увеличение мышечной массы. Используются умеренные веса (60-80% от 1ПМ – одноповторный максимум) с большим количеством повторений (8-12). Общий объем тренировок высокий.</li>
            <li><b>Фаза силы:</b> Цель – развитие максимальной силы. Веса увеличиваются (80-90% от 1ПМ), а количество повторений уменьшается (4-6). Объем тренировок снижается, а интенсивность возрастает.</li>
            <li><b>Фаза мощности (пиковая):</b> Сосредоточение на скорости и взрывной силе. Используются меньшие веса (70-85% от 1ПМ) с небольшим количеством повторений (1-3), выполняемых максимально быстро. Основной акцент на технических аспектах движения.</li>
        </ul>
        <p><b>Пример:</b><br>
        Месяц 1-3: Гипертрофия (8-12 повторений, умеренные веса)<br>
        Месяц 4-6: Сила (4-6 повторений, большие веса)<br>
        Месяц 7-9: Мощность (1-3 повторения, быстрые движения)</p>
        <p><b>Преимущества:</b></p>
        <ul>
            <li>Простота в понимании и применении.</li>
            <li>Подходит для новичков и тех, кто хочет нарастить мышечную массу и силу.</li>
        </ul>
        <p><b>Недостатки:</b></p>
        <ul>
            <li>Может привести к плато, так как организм адаптируется к однообразной нагрузке.</li>
            <li>Развивает физические качества последовательно, а не одновременно.</li>
        </ul>
        <p><b>Рекомендации для приложения:</b></p>
        <ul>
            <li>Идеально подходит для создания простых тренировочных программ для начинающих.</li>
            <li>Легко визуализировать графики прогресса (увеличение веса, количества повторений).</li>
            <li>Может быть дополнена функцией автоматического увеличения веса от тренировки к тренировке.</li>
        </ul>

        <h3>2. Волновая (волнообразная) периодизация (Undulating Periodization)</h3>
        <p><b>Описание:</b> Нагрузка варьируется в пределах недели или микроцикла. Существует два основных подхода:</p>
        <ul>
            <li><b>Недельная волновая периодизация:</b> Каждая неделя тренировок имеет свою цель (например, неделя гипертрофии, неделя силы, неделя мощности).</li>
            <li><b>Дневная волновая периодизация:</b> В течение одной недели тренировки чередуются по типу нагрузки (например, день гипертрофии, день силы, день мощности).</li>
        </ul>
        <p><b>Пример:</b><br>
        Неделя 1: Гипертрофия (8-12 повторений)<br>
        Неделя 2: Сила (4-6 повторений)<br>
        Неделя 3: Мощность (1-3 повторения)<br>
        Повторить цикл.</p>
        <p><b>Преимущества:</b></p>
        <ul>
            <li>Более эффективна, чем линейная периодизация, особенно для опытных спортсменов.</li>
            <li>Предотвращает адаптацию организма к однообразной нагрузке.</li>
            <li>Позволяет развивать разные физические качества одновременно.</li>
        </ul>
        <p><b>Недостатки:</b></p>
        <ul>
            <li>Более сложная в планировании и реализации.</li>
            <li>Требует более тщательного контроля за восстановлением.</li>
        </ul>
        <p><b>Рекомендации для приложения:</b></p>
        <ul>
            <li>Подходит для создания более продвинутых тренировочных программ.</li>
            <li>Требует более сложного алгоритма для планирования тренировок.</li>
            <li>Необходимо учитывать индивидуальные особенности пользователя (уровень подготовки, цели, восстановление).</li>
        </ul>

        <h3>3. Блоковая периодизация (Block Periodization)</h3>
        <p><b>Описание:</b> Тренировочный процесс разделяется на отдельные блоки (обычно 2-4 недели), каждый из которых имеет свою четкую цель (например, накопление, трансформация, реализация). Каждый блок фокусируется на развитии одного или двух ключевых физических качеств.</p>
        <ul>
            <li><b>Блок накопления (accumulation):</b> Создание фундамента для дальнейшего прогресса. Высокий объем тренировок, умеренная интенсивность. Развитие общей физической подготовки и выносливости.</li>
            <li><b>Блок трансформации (transmutation):</b> Преобразование накопленного потенциала в специфические физические качества (например, сила, мощность). Снижение объема тренировок, увеличение интенсивности.</li>
            <li><b>Блок реализации (realization):</b> Сосредоточение на достижении пиковых результатов. Максимальная интенсивность, минимальный объем тренировок. Оптимизация техники и тактики.</li>
        </ul>
        <p><b>Пример:</b><br>
        Блок 1 (4 недели): Накопление (развитие общей физической подготовки)<br>
        Блок 2 (4 недели): Трансформация (развитие силы)<br>
        Блок 3 (2 недели): Реализация (достижение пиковой формы)</p>
        <p><b>Преимущества:</b></p>
        <ul>
            <li>Позволяет максимально концентрироваться на развитии конкретных физических качеств.</li>
            <li>Эффективна для достижения высоких спортивных результатов.</li>
        </ul>
        <p><b>Недостатки:</b></p>
        <ul>
            <li>Наиболее сложная в планировании и реализации.</li>
            <li>Требует очень точного контроля за нагрузкой и восстановлением.</li>
            <li>Подходит только для опытных спортсменов.</li>
        </ul>
        <p><b>Рекомендации для приложения:</b></p>
        <ul>
            <li>Подходит для создания тренировочных программ для продвинутых пользователей, стремящихся к максимальным результатам.</li>
            <li>Требует глубокого понимания принципов тренировки и физиологии.</li>
            <li>Рекомендуется использовать только под контролем опытного тренера.</li>
        </ul>
        """)
        periodization_layout.addWidget(periodization_text)
        periodization_tab.setLayout(periodization_layout)


        balanced_nutrition_tab = QWidget()
        balanced_layout = QVBoxLayout()
        balanced_text = QTextEdit()
        balanced_text.setReadOnly(True)
        balanced_text.setHtml("""
        <h2 style="color: #ff3333;">Сбалансированное питание</h2>
        <p><b>Сбалансированное питание</b> — это основа здоровья, энергии и хорошего самочувствия. Правильный рацион обеспечивает организм необходимыми питательными веществами для поддержания всех функций и достижения оптимальной производительности.</p>

        <p>В этой статье мы рассмотрим основные компоненты здорового питания и дадим практические рекомендации, которые помогут вам сделать осознанный выбор продуктов и составить сбалансированное меню.</p>

        <h3>1. Белки (Протеины): Строительные блоки организма</h3>
        <p><b>Роль:</b> Белки необходимы для построения и восстановления тканей, производства ферментов и гормонов, а также для поддержания иммунной системы.</p>
        <p><b>Источники:</b></p>
        <ul>
            <li><b>Животные:</b> Мясо (птица, говядина, свинина), рыба, яйца, молочные продукты (молоко, творог, йогурт, сыр).</li>
            <li><b>Растительные:</b> Бобовые (фасоль, горох, чечевица, нут), тофу, киноа, орехи и семена.</li>
        </ul>
        <p><b>Рекомендации:</b> Старайтесь включать белок в каждый прием пищи. Выбирайте нежирные источники белка (например, куриную грудку, рыбу, творог с низким содержанием жира). Сочетайте животные и растительные источники белка для получения полного набора аминокислот.</p>
        <p><b>Когда есть:</b> Равномерно распределяйте потребление белка в течение дня. Особенно важен белок на завтрак и после физической активности для восстановления мышц.</p>

        <h3>2. Жиры (Липиды): Энергия и гормональный баланс</h3>
        <p><b>Роль:</b> Жиры являются важным источником энергии, необходимы для усвоения витаминов, производства гормонов и поддержания здоровья кожи и волос.</p>
        <p><b>Типы:</b></p>
        <ul>
            <li><b>Насыщенные:</b> Содержатся в основном в продуктах животного происхождения (жирное мясо, сливочное масло, сыр) и некоторых растительных маслах (кокосовое, пальмовое). Потребление насыщенных жиров следует ограничивать.</li>
            <li><b>Ненасыщенные:</b> Содержатся в растительных маслах (оливковое, льняное, подсолнечное), орехах, семенах и рыбе. Ненасыщенные жиры полезны для здоровья сердца и сосудов.</li>
            <li><b>Полиненасыщенные жирные кислоты (ПНЖК):</b> Омега-3 и омега-6 – незаменимые жирные кислоты, которые организм не может производить самостоятельно и должен получать из пищи.</li>
        </ul>
        <p><b>Источники:</b></p>
        <ul>
            <li>Растительные масла (оливковое, льняное, авокадо)</li>
            <li>Орехи и семена (миндаль, грецкий орех, чиа, лен)</li>
            <li>Авокадо</li>
            <li>Жирная рыба (лосось, скумбрия, сардины)</li>
        </ul>
        <p><b>Рекомендации:</b> Выбирайте ненасыщенные жиры вместо насыщенных и трансжиров. Используйте растительные масла для заправки салатов и приготовления пищи. Включайте в рацион орехи, семена и жирную рыбу.</p>
        <p><b>Когда есть:</b> В умеренных количествах добавляйте полезные жиры в каждый прием пищи.</p>

        <h3>3. Углеводы: Основной источник энергии</h3>
        <p><b>Роль:</b> Углеводы являются основным источником энергии для организма, особенно для мозга и мышц.</p>
        <p><b>Типы:</b></p>
        <ul>
            <li><b>Простые (быстрые):</b> Содержатся в сладостях, выпечке, белом хлебе, газированных напитках. Быстро усваиваются, вызывая резкий скачок уровня сахара в крови.</li>
            <li><b>Сложные (медленные):</b> Содержатся в цельнозерновых продуктах (коричневый рис, овсянка, гречка, цельнозерновой хлеб), овощах, фруктах и бобовых. Усваиваются медленно, обеспечивая организм энергией на длительный период.</li>
        </ul>
        <p><b>Источники:</b></p>
        <ul>
            <li>Цельнозерновые продукты</li>
            <li>Овощи</li>
            <li>Фрукты</li>
            <li>Бобовые</li>
        </ul>
        <p><b>Рекомендации:</b> Отдавайте предпочтение сложным углеводам. Ограничивайте потребление простых углеводов и сахара. Включайте в рацион разнообразные овощи и фрукты.</p>
        <p><b>Когда есть:</b> Ешьте сложные углеводы в течение дня, особенно утром и перед физической активностью. Ограничьте потребление простых углеводов вечером.</p>

        <h3>Что лучше исключить или ограничить:</h3>
        <ul>
            <li><b>Трансжиры:</b> Содержатся в обработанных продуктах (фаст-фуд, выпечка, маргарин). Повышают риск сердечно-сосудистых заболеваний.</li>
            <li><b>Добавленный сахар:</b> Содержится в сладостях, газированных напитках, соках. Приводит к набору веса, развитию диабета и других заболеваний.</li>
            <li><b>Обработанные продукты:</b> Содержат много соли, сахара, трансжиров и искусственных добавок. Старайтесь выбирать цельные, необработанные продукты.</li>
            <li><b>Фаст-фуд:</b> Содержит много калорий, жиров и соли, но мало питательных веществ.</li>
        </ul>

        <h3>Общие рекомендации:</h3>
        <ul>
            <li><b>Пейте достаточно воды:</b> Вода необходима для поддержания всех функций организма. Старайтесь выпивать не менее 1,5-2 литров воды в день.</li>
            <li><b>Ешьте разнообразную пищу:</b> Разнообразный рацион обеспечивает организм всеми необходимыми витаминами и минералами.</li>
            <li><b>Слушайте свой организм:</b> Ешьте, когда голодны, и останавливайтесь, когда насытились.</li>
            <li><b>Готовьте дома:</b> Приготовление пищи дома позволяет контролировать ингредиенты и избегать вредных добавок.</li>
            <li><b>Планируйте свои приемы пищи:</b> Планирование помогает сделать осознанный выбор продуктов и избегать перекусов вредной пищей.</li>
            <li><b>Не забывайте о клетчатке:</b> Клетчатка содержится в овощах, фруктах, цельнозерновых продуктах и бобовых. Она улучшает пищеварение, снижает уровень холестерина и контролирует уровень сахара в крови.</li>
        </ul>

        <h3>Когда лучше есть:</h3>
        <ul>
            <li><b>Завтрак:</b> Важный прием пищи, который запускает метаболизм и обеспечивает организм энергией на первую половину дня. Включайте белок, сложные углеводы и полезные жиры.</li>
            <li><b>Обед:</b> Умеренный прием пищи, который поддерживает уровень энергии в течение дня. Включайте белок, сложные углеводы и овощи.</li>
            <li><b>Ужин:</b> Легкий прием пищи, который не перегружает пищеварительную систему перед сном. Включайте белок и овощи.</li>
            <li><b>Перекусы:</b> Полезные перекусы между основными приемами пищи помогают поддерживать уровень сахара в крови и избегать переедания. Выбирайте фрукты, орехи, йогурт или овощные палочки.</li>
        </ul>
        """)
        balanced_layout.addWidget(balanced_text)
        balanced_nutrition_tab.setLayout(balanced_layout)


        self.tabs.addTab(sports_nutrition_tab, "Спортивное питание")
        self.tabs.addTab(periodization_tab, "Периодизация")
        self.tabs.addTab(balanced_nutrition_tab, "Сбалансированное питание")
        layout.addWidget(self.tabs)
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)

class FitnessApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Фитнес-приложение")
        self.setFixedSize(600, 400)
        self.setStyleSheet(APP_STYLE)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        title_label = QLabel("Фитнес-приложение")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ff3333;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addStretch(1)
        self.trainings_btn = QPushButton("Тренировки")
        self.trainings_btn.setStyleSheet("font-size: 16px; padding: 15px;")
        self.trainings_btn.clicked.connect(self.open_trainings)
        self.bju_btn = QPushButton("Калькулятор БЖУ")
        self.bju_btn.setStyleSheet("font-size: 16px; padding: 15px;")
        self.bju_btn.clicked.connect(self.open_bju)
        self.reference_btn = QPushButton("Справочная информация")
        self.reference_btn.setStyleSheet("font-size: 16px; padding: 15px;")
        self.reference_btn.clicked.connect(self.open_reference)
        layout.addWidget(self.trainings_btn)
        layout.addWidget(self.bju_btn)
        layout.addWidget(self.reference_btn)
        layout.addStretch(1)
        exit_button = QPushButton("Выход")
        exit_button.setStyleSheet("font-size: 14px; padding: 10px;")
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)
        self.setLayout(layout)

    def open_trainings(self):
        trainings_window = TrainingsWindow()
        trainings_window.exec_()

    def open_bju(self):
        bju_window = BjuWindow()
        bju_window.exec_()

    def open_reference(self):
        reference_window = ReferenceWindow()
        reference_window.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  
    visual = QPalette()
    visual.setColor(QPalette.Window, QColor(30, 30, 30))
    visual.setColor(QPalette.WindowText, Qt.white)
    visual.setColor(QPalette.Base, QColor(42, 42, 42))
    visual.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    visual.setColor(QPalette.ToolTipBase, Qt.white)
    visual.setColor(QPalette.ToolTipText, Qt.white)
    visual.setColor(QPalette.Text, Qt.white)
    visual.setColor(QPalette.Button, QColor(53, 53, 53))
    visual.setColor(QPalette.ButtonText, Qt.white)
    visual.setColor(QPalette.BrightText, Qt.red)
    visual.setColor(QPalette.Link, QColor(112, 0, 24))
    visual.setColor(QPalette.Highlight, QColor(112, 0, 24))
    visual.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(visual)
    window = FitnessApp()
    window.show()
    sys.exit(app.exec_())