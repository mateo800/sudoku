from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QLabel, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys

class CeldaSudoku(QLineEdit):
    def __init__(self, fila, columna, ventana_padre):
        super().__init__()
        self.fila = fila
        self.columna = columna
        self.ventana_padre = ventana_padre
        self.es_celda_inicial = False
        
        self.setMaxLength(1)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(60, 60)
        
        fuente = QFont("Segoe UI", 22, QFont.Bold)
        self.setFont(fuente)
        self.bordes_originales = self.calcular_bordes() 
        self.aplicar_estilo_editable()
        self.textChanged.connect(self.validar_entrada)
    
    def calcular_bordes(self):
        borde_derecho = "5px" if (self.columna + 1) % 3 == 0 and self.columna != 8 else "1px"
        borde_inferior = "5px" if (self.fila + 1) % 3 == 0 and self.fila != 8 else "1px"
        borde_izquierdo = "5px" if self.columna % 3 == 0 and self.columna != 0 else "1px"
        borde_superior = "5px" if self.fila % 3 == 0 and self.fila != 0 else "1px"
        return {
            'superior': borde_superior,
            'inferior': borde_inferior,
            'izquierdo': borde_izquierdo,
            'derecho': borde_derecho
        }
    
    def validar_entrada(self, texto):
        if texto and not texto.isdigit():
            self.setText("")
        elif texto and (int(texto) < 1 or int(texto) > 9):
            self.setText("")
        else:
            if not self.es_celda_inicial:
                self.aplicar_estilo_editable()
    
    def aplicar_estilo_editable(self):
        bordes = self.bordes_originales
        estilo = f"""
            QLineEdit {{
                background-color: white;
                border-top: {bordes['superior']} solid #2c3e50;
                border-bottom: {bordes['inferior']} solid #2c3e50;
                border-left: {bordes['izquierdo']} solid #2c3e50;
                border-right: {bordes['derecho']} solid #2c3e50;
                color: #1a1a1a;
                font-weight: 600;
            }}
            QLineEdit:focus {{
                background-color: #e3f2fd;
            }}
        """
        self.setStyleSheet(estilo)
        self.setReadOnly(False)
        self.es_celda_inicial = False
    
    def aplicar_estilo_inicial(self):
        bordes = self.bordes_originales
        estilo = f"""
            QLineEdit {{
                background-color: #f8f9fa;
                border-top: {bordes['superior']} solid #2c3e50;
                border-bottom: {bordes['inferior']} solid #2c3e50;
                border-left: {bordes['izquierdo']} solid #2c3e50;
                border-right: {bordes['derecho']} solid #2c3e50;
                color: #667eea;
                font-weight: 700;
            }}
        """
        self.setStyleSheet(estilo)
        self.setReadOnly(True)
        self.es_celda_inicial = True
    
    def aplicar_estilo_solucion(self):
        bordes = self.bordes_originales
        estilo = f"""
            QLineEdit {{
                background-color: #e8f5e9;
                border-top: {bordes['superior']} solid #2c3e50;
                border-bottom: {bordes['inferior']} solid #2c3e50;
                border-left: {bordes['izquierdo']} solid #2c3e50;
                border-right: {bordes['derecho']} solid #2c3e50;
                color: #2e7d32;
                font-weight: 600;
            }}
        """
        self.setStyleSheet(estilo)
    
    def aplicar_estilo_error(self):
        bordes = self.bordes_originales
        estilo = f"""
            QLineEdit {{
                background-color: #ffebee;
                border-top: {bordes['superior']} solid #e74c3c;
                border-bottom: {bordes['inferior']} solid #e74c3c;
                border-left: {bordes['izquierdo']} solid #e74c3c;
                border-right: {bordes['derecho']} solid #e74c3c;
                color: #c62828;
                font-weight: 600;
            }}
        """
        self.setStyleSheet(estilo)
    
    def obtener_valor(self):
        texto = self.text()
        return int(texto) if texto else 0
    
    def establecer_valor(self, valor):
        self.setText(str(valor) if valor != 0 else "")
    
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        
        nueva_fila = self.fila
        nueva_columna = self.columna
        
        if event.key() == Qt.Key_Up and self.fila > 0:
            nueva_fila = self.fila - 1
        elif event.key() == Qt.Key_Down and self.fila < 8:
            nueva_fila = self.fila + 1
        elif event.key() == Qt.Key_Left and self.columna > 0:
            nueva_columna = self.columna - 1
        elif event.key() == Qt.Key_Right and self.columna < 8:
            nueva_columna = self.columna + 1
        
        if nueva_fila != self.fila or nueva_columna != self.columna:
            self.ventana_padre.celdas[nueva_fila][nueva_columna].setFocus()


class VentanaSudoku(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver")
        self.setFixedSize(700, 820)
        
        self.celdas = [[None for _ in range(9)] for _ in range(9)]
        self.tablero_inicial = [[0 for _ in range(9)] for _ in range(9)]
        
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(25)
        widget_central.setLayout(layout_principal)
        
        titulo = QLabel("SUDOKU")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Segoe UI", 36, QFont.Bold))
        titulo.setStyleSheet("color: #fffff; margin-bottom: 10px;")
        layout_principal.addWidget(titulo)
        
        frame_tablero = QFrame()
        frame_tablero.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        layout_frame = QVBoxLayout()
        frame_tablero.setLayout(layout_frame)
        
        layout_tablero = self.crear_tablero()
        layout_frame.addLayout(layout_tablero)
        
        layout_principal.addWidget(frame_tablero)
        
        layout_botones = self.crear_botones()
        layout_principal.addLayout(layout_botones)

        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #764ba2, stop:1 #667eea);
            }
        """)
    
    def crear_tablero(self):
        layout_tablero = QGridLayout()
        layout_tablero.setSpacing(1)
        
        for fila in range(9):
            for columna in range(9):
                celda = CeldaSudoku(fila, columna, self)
                self.celdas[fila][columna] = celda
                layout_tablero.addWidget(celda, fila, columna)
        
        return layout_tablero
    
    def crear_botones(self):
        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(15)
        
        boton_resolver = QPushButton("Resolver")
        boton_resolver.setFont(QFont("Segoe UI", 14, QFont.Bold))
        boton_resolver.setFixedHeight(55)
        boton_resolver.setCursor(Qt.PointingHandCursor)
        boton_resolver.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3, stop:1 #6a3f8f);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a56bd, stop:1 #5d357d);
            }
        """)
        boton_resolver.clicked.connect(self.resolver_sudoku)
        
        boton_validar = QPushButton("Validar")
        boton_validar.setFont(QFont("Segoe UI", 14, QFont.Bold))
        boton_validar.setFixedHeight(55)
        boton_validar.setCursor(Qt.PointingHandCursor)
        boton_validar.setStyleSheet("""
            QPushButton {
                background-color: #48bb78;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #38a169;
            }
            QPushButton:pressed {
                background-color: #2f855a;
            }
        """)
        boton_validar.clicked.connect(self.validar_tablero)
        
        boton_limpiar = QPushButton("Reiniciar")
        boton_limpiar.setFont(QFont("Segoe UI", 14, QFont.Bold))
        boton_limpiar.setFixedHeight(55)
        boton_limpiar.setCursor(Qt.PointingHandCursor)
        boton_limpiar.setStyleSheet("""
            QPushButton {
                background-color: #fc8181;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #f56565;
            }
            QPushButton:pressed {
                background-color: #e53e3e;
            }
        """)
        boton_limpiar.clicked.connect(self.limpiar_tablero)
        
        layout_botones.addWidget(boton_resolver)
        layout_botones.addWidget(boton_validar)
        layout_botones.addWidget(boton_limpiar)
        
        return layout_botones
    
    def obtener_tablero_actual(self):
        tablero = []
        for fila in range(9):
            fila_valores = []
            for columna in range(9):
                valor = self.celdas[fila][columna].obtener_valor()
                fila_valores.append(valor)
            tablero.append(fila_valores)
        return tablero
    
    def establecer_tablero(self, tablero):
        for fila in range(9):
            for columna in range(9):
                valor = tablero[fila][columna]
                self.celdas[fila][columna].establecer_valor(valor)
    
    def guardar_tablero_inicial(self):
        self.tablero_inicial = [[self.celdas[fila][columna].obtener_valor() 
                                for columna in range(9)] 
                                for fila in range(9)]
    
    def es_movimiento_valido(self, tablero, fila, columna, numero):
        for col in range(9):
            if tablero[fila][col] == numero:
                return False
        
        for fil in range(9):
            if tablero[fil][columna] == numero:
                return False

        inicio_fila = (fila // 3) * 3
        inicio_columna = (columna // 3) * 3
        
        for fil in range(inicio_fila, inicio_fila + 3):
            for col in range(inicio_columna, inicio_columna + 3):
                if tablero[fil][col] == numero:
                    return False
        
        return True
    
    def resolver(self, tablero):
        # Buscar la siguiente celda vacía
        for fila in range(9):
            for columna in range(9):
                if tablero[fila][columna] == 0:
                    # Intentar números del 1 al 9
                    for numero in range(1, 10):
                        if self.es_movimiento_valido(tablero, fila, columna, numero):
                            # Colocar el número
                            tablero[fila][columna] = numero
                            
                            # Intentar resolver recursivamente
                            if self.resolver(tablero):
                                return True
                            
                            # Si no funciona, retroceder (backtrack)
                            tablero[fila][columna] = 0
                    
                    # Si ningún número funciona, retroceder
                    return False
        
        # Si no hay celdas vacías, el Sudoku está resuelto
        return True
    
    def resolver_sudoku(self):
        tablero = self.obtener_tablero_actual()
        
        self.guardar_tablero_inicial()
        
        tablero_copia = [fila[:] for fila in tablero]
        
        for fila in range(9):
            for columna in range(9):
                if tablero[fila][columna] != 0:
                    self.celdas[fila][columna].aplicar_estilo_inicial()
        
        if self.resolver(tablero_copia):
            for fila in range(9):
                for columna in range(9):
                    if tablero[fila][columna] == 0:  # Era una celda vacía
                        self.celdas[fila][columna].establecer_valor(tablero_copia[fila][columna])
                        self.celdas[fila][columna].aplicar_estilo_solucion()
            
            QMessageBox.information(self, "Resuelto", "El Sudoku ha sido resuelto exitosamente")
        else:
            QMessageBox.warning(self, "Sin solución", "No se encontró una solución válida para este Sudoku")
    
    def validar_tablero(self):
        tablero = self.obtener_tablero_actual()
        errores_encontrados = False
        
        for fila in range(9):
            for columna in range(9):
                if self.celdas[fila][columna].es_celda_inicial:
                    self.celdas[fila][columna].aplicar_estilo_inicial()
                else:
                    self.celdas[fila][columna].aplicar_estilo_editable()

        for fila in range(9):
            for columna in range(9):
                valor = tablero[fila][columna]
                if valor != 0:
                    tablero[fila][columna] = 0
                    
                    if not self.es_movimiento_valido(tablero, fila, columna, valor):
                        self.celdas[fila][columna].aplicar_estilo_error()
                        errores_encontrados = True
                    
                    tablero[fila][columna] = valor
        
        if errores_encontrados:
            QMessageBox.warning(self, "Errores encontrados", "Hay números duplicados en filas, columnas o subcuadrículas")
        else:
            QMessageBox.information(self, "Validación exitosa", "No se encontraron errores El Sudoku es válido")
    
    def limpiar_tablero(self):
        for fila in range(9):
            for columna in range(9):
                self.celdas[fila][columna].establecer_valor(0)
                self.celdas[fila][columna].aplicar_estilo_editable()
        
        self.tablero_inicial = [[0 for _ in range(9)] for _ in range(9)]


def main():
    aplicacion = QApplication(sys.argv)
    ventana = VentanaSudoku()
    ventana.show()
    sys.exit(aplicacion.exec())


if __name__ == "__main__":
    main()