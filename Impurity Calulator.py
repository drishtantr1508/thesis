import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QLineEdit, QPushButton, QLabel, QSpacerItem, QSizePolicy, QMessageBox, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt

class ExampleApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle('Impurity Predictor')
        self.setGeometry(100, 100, 600, 400)

        # Create main layout
        main_layout = QVBoxLayout()

        # Add combobox for model selection
        self.model_selector = QComboBox(self)
        self.model_selector.addItems(["Model 1", "Model 2", "Model 3"])  # Add your model names here
        model_layout = QHBoxLayout()
        model_layout.addStretch()
        model_layout.addWidget(self.model_selector)
        model_layout.addStretch()
        main_layout.addLayout(model_layout)

        # Create grid layout for inputs and labels
        grid_layout = QGridLayout()

        # Create input fields with labels below
        self.inputs = {}
        labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

        positions = [(i, j) for i in range(4) for j in range(3)]  # Define positions for the first 12 labels

        for position, label in zip(positions, labels):
            row, col = position
            vbox = QVBoxLayout()
            self.inputs[label] = QLineEdit(self)
            self.inputs[label].setText('0')  # Default value set to zero
            self.inputs[label].installEventFilter(self)  # Install event filter for focus
            input_label = QLabel(label, self)
            input_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)  # Center align the label horizontally
            vbox.addWidget(self.inputs[label])
            vbox.addWidget(input_label)
            grid_layout.addLayout(vbox, row, col)

        # Add the grid layout to the main layout
        main_layout.addLayout(grid_layout)

        # Add the target field
        self.target = QLineEdit(self)
        self.target.setFixedSize(400, 30)  # Fixed size to prevent resizing
        target_layout = QVBoxLayout()
        target_label = QLabel('Target', self)
        target_label.setAlignment(Qt.AlignHCenter)
        target_layout.addWidget(target_label)
        target_layout.addWidget(self.target)
        target_layout.setAlignment(Qt.AlignCenter)

        # Add the Predict button
        self.predict_button = QPushButton('Predict', self)
        self.predict_button.setStyleSheet('background-color: blue; color: white')
        self.predict_button.clicked.connect(self.calculate_sum)

        # Add layouts to ensure central alignment
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.predict_button)
        button_layout.addStretch()

        # Add target layout and button layout to the main layout
        main_layout.addLayout(target_layout)
        main_layout.addLayout(button_layout)

        # Set the main layout
        self.setLayout(main_layout)

    def eventFilter(self, source, event):
        if event.type() == event.FocusIn:
            if source.text() == '0':
                source.clear()
        return super().eventFilter(source, event)

    def calculate_sum(self):
        total_sum = 0
        try:
            for key in self.inputs:
                total_sum += float(self.inputs[key].text())
            selected_model = self.model_selector.currentText()
            self.target.setText(f"{selected_model}: {total_sum}")
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Please enter valid numbers')

def main():
    app = QApplication(sys.argv)
    ex = ExampleApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
