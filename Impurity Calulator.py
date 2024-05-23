import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QVBoxLayout, QLineEdit, 
    QPushButton, QLabel, QSpacerItem, QSizePolicy, QMessageBox, 
    QHBoxLayout, QComboBox
)
from PyQt5.QtCore import Qt
import numpy as np 
import pickle
from sklearn.linear_model import LinearRegression

class ExampleApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle('Impurity Predictor')
        self.setGeometry(100, 100, 800, 600)

        # Create main layout
        main_layout = QVBoxLayout()

        # Add combobox for model selection
        self.model_selector = QComboBox(self)
        self.model_selector.addItems([
            "Linear Regression", "Ridge", "Lasso", "ElasticNet",
            "Decision Tree", "Random Forest", "Gradient Boosting"
        ])
        model_layout = QHBoxLayout()
        model_layout.addStretch()
        model_layout.addWidget(self.model_selector)
        model_layout.addStretch()
        main_layout.addLayout(model_layout)

        # Create grid layout for inputs and labels
        grid_layout = QGridLayout()

        # New feature set
        self.inputs = {}
        labels = [
            '% Iron Feed', '% Silica Feed', 'Starch Flow', 'Amina Flow', 
            'Ore Pulp Flow', 'Ore Pulp pH', 'Ore Pulp Density', 
            'Flotation Column 01 Air Flow', 'Flotation Column 02 Air Flow', 
            'Flotation Column 03 Air Flow', 'Flotation Column 04 Air Flow', 
            'Flotation Column 05 Air Flow', 'Flotation Column 06 Air Flow', 
            'Flotation Column 07 Air Flow', 'Flotation Column 01 Level', 
            'Flotation Column 02 Level', 'Flotation Column 03 Level', 
            'Flotation Column 04 Level', 'Flotation Column 05 Level', 
            'Flotation Column 06 Level', 'Flotation Column 07 Level', 
            '% Iron Concentrate'
        ]

        positions = [(i, j) for i in range(8) for j in range(3)]  # Define positions for the new labels

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
        target_label = QLabel('% Silica Concentrate', self)
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
        try:
            train_arr = []
            loaded_model = LinearRegression()
            for key in self.inputs:
                train_arr.append((float(self.inputs[key].text())))
            train_arr = np.array(train_arr).reshape(1,22)
            selected_model = self.model_selector.currentText()
        
            if selected_model == "Linear Regression":
                with open('models/lr_model.pkl', 'rb') as file:
                    loaded_model = pickle.load(file)
            elif selected_model == "Ridge":
                with open('models/rd_model.pkl', 'rb') as file:
                    loaded_model = pickle.load(file)
            elif selected_model == "Lasso":
                with open('models/ls_model.pkl', 'rb') as file:
                    loaded_model = pickle.load(file)
            elif selected_model == "ElasticNet":
                with open('models/en_model.pkl', 'rb') as file:
                    loaded_model = pickle.load(file)
            elif selected_model == "Decision Tree":
                with open('models/dt_model.pkl', 'rb') as file:
                    loaded_model = pickle.load(file)
            elif selected_model == "Random Forest":
                with open('models/rf_model.pkl', 'rb') as file:
                    loaded_model = pickle.load(file)
            else:
                with open('models/gb_model.pkl', 'rb') as file:
                    loaded_model = pickle.load(file)
                
            target = loaded_model.predict(train_arr)[0]
            self.target.setText(f"{selected_model}: {target}")
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Please enter valid numbers')

def main():
    app = QApplication(sys.argv)
    ex = ExampleApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
