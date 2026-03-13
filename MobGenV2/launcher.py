import sys
sys.path.append(r"C:\Users\AT280565\PycharmProjects\Perso\RepoMob\MobGenV2")
from RepoMob.MobGenV2 import LEVEL, MOB_TYPE, STATS, SCRIPT_DIR
from RepoMob.MobGenV2.class_mob import Mob
from RepoMob.MobGenV2.utils import flat2dice, flat2complexite
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QGridLayout, QLabel, QLineEdit,
    QFrame, QComboBox,
)

from PyQt5.QtGui import (
    QIcon
)

from PyQt5.QtCore import (
    Qt
)


class QSheet(QWidget):
    def __init__(self, mob: Mob):
        super().__init__()
        self.mob = mob
        self.values = {
            "name": self.mob.name,
            "floor": self.mob.level,
            "mob_type": self.mob.mob_type,
            "main_stat": self.mob.main_stat,
            "stats": self.mob.stats,
            "danger": self.mob.danger,
            "exp": self.mob.exp,
            "gold": self.mob.gold,
            "lp": self.mob.lp,
            "mean_dmg": self.mob.mean_dmg,
            "max_dmg": self.mob.max_dmg,
            "mean_cmplx": self.mob.mean_cmplx,
            "max_cmplx": self.mob.max_cmplx,
            "mob_nbr": self.mob.mob_nbr,
            "ca": self.mob.ca,
            "ce": self.mob.ce,
            "sd": self.mob.sd
        }

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.build_header()
        self.build_stat()
        self.build_rewards()
        self.build_moveset()

    def build_header(self):
        mob_name = self.values["name"]
        label_name = QLabel(
            f"""
            <h1>{mob_name} : {self.values["lp"]} HP ({flat2dice(self.values["lp"])})</h1></br>
            <h3>Spécificité</h3></br>
            <ul>
                <li>Étage  : {self.values["floor"]}</li>
                <li>Type   : {self.values["mob_type"]}</li>
                <li>Danger : {self.values["danger"]}</li>
                <li>Rencontre : {self.values["mob_nbr"]}</li>
            </ul>
            """
        )
        self.layout.addWidget(
            label_name,
            0, 0,
            1, 1
        )

    def build_stat(self):
        stats = self.values["stats"]

        row1 = ""
        row2 = ""
        for stat_name, stat_value in stats.items():
            if stat_name == self.values["main_stat"]:
                row1 += f"""<td style="text-align:center;"><b>{stat_name[:3].upper()}</b></td>"""
                row2 += f"""<td style="text-align:center;"><b>{stat_value}</b></td>"""
            else:
                row1 += f"""<td style="text-align:center;">{stat_name[:3].upper()}</td>"""
                row2 += f"""<td style="text-align:center;">{stat_value}</td>"""

        table_stats = f"""
        <h3>Caractéristiques - Scores</h3></br>
        <div style="text-align:center;">
            <table border="1" cellpadding="4" cellspacing="0">
                <tr>{row1}</tr>
                <tr>{row2}</tr>
            </table>
        </div>
        """

        row1 = ""
        row2 = ""
        score = {
            "CA": self.values["ca"],
            "CE": self.values["ce"],
            "SD": self.values["sd"]
        }
        for score_name, score_value in score.items():
            row1 += f"""<td style="text-align:center;">{score_name}</td>"""
            row2 += f"""<td style="text-align:center;">{score_value}</td>"""
        table_stats += f"""
        <div style="text-align:center;">
            <table border="1" cellpadding="4" cellspacing="0">
                <tr>{row1}</tr>
                <tr>{row2}</tr>
            </table>
        </div>
        """

        label_stats = QLabel(table_stats)
        # label_stats.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(
            label_stats,
            1, 0,
            1, 1
        )

    def build_rewards(self):
        gold = self.values["gold"]
        experience = self.values["exp"]

        label_rewards = QLabel(
            f"""
                <h3>Récompenses :</h3>
                <ul>
                    <li>Pièces d'or  : {gold}</li>
                    <li>Expérience   : {experience}</li>
                </ul>
            """
        )
        self.layout.addWidget(
            label_rewards,
            2, 0,
            1, 1
        )


    def build_moveset(self):
        mean_dmg = self.values["mean_dmg"]
        max_dmg = self.values["max_dmg"]
        mean_cmplx = self.values["mean_cmplx"]
        max_cmplx = self.values["max_cmplx"]

        label_damage = QLabel(
            f"""
                <h3>Actions & Effets :</h3>
                <table>
                    <tr>
                        <td valign="top">
                            <ul>
                                <li>Dégâts moyens : {mean_dmg} ({flat2dice(mean_dmg)})</li>
                                <li>Dégâts max    : {max_dmg} ({flat2dice(max_dmg)})</li>
                            </ul>
                        </td>
                        <td style="padding-left: 40px;" valign="top">
                            <ul>
                                <li>Complexité moyenne : {mean_cmplx} ({flat2complexite(mean_dmg)})</li>
                                <li>Complexité max     : {max_cmplx} ({flat2complexite(max_dmg)})</li>
                            </ul>
                        </td>
                    </tr>
                </table>
            """
        )
        self.layout.addWidget(
            label_damage,
            3, 0,
            1, 1
        )


class MaFenetre(QWidget):
    def __init__(self):
        # Setting up attributes
        super().__init__()
        self.name = None
        self.box_stat = None
        self.box_type = None
        self.box_floor = None

        self.mob = None
        self.mob_sheet = None

        # Setting up the window
        self.setWindowTitle("Générateur de mob")
        # self.setWindowIcon(QIcon(str(SCRIPT_DIR / "Images" / "babel.ico")))
        self.resize(300, 100)

        self.layout = QGridLayout()
        self.layout.setColumnStretch(1, 5)
        self.layout.setColumnStretch(0, 1)
        self.setLayout(self.layout)

        # Left Panel
        self.left_panel = QFrame()
        self.left_panel.setFrameShape(QFrame.StyledPanel)
        self.left_panel.setStyleSheet(
            """
                QFrame {
                    background-color: #f0f0f0;
                    border: 2px solid #a0a0a0;
                    border-radius: 10px;
                    padding: 10px;
                }
            """)
        self.left_panel_layout = QGridLayout()
        self.left_panel.setLayout(self.left_panel_layout)

        # Right Panel
        self.right_panel = QFrame()
        self.right_panel.setFrameShape(QFrame.StyledPanel)
        self.right_panel.setStyleSheet(
            """
                QFrame {
                    background-color: #f0f0f0;
                    border: 2px solid #a0a0a0;
                    border-radius: 10px;
                    padding: 10px;
                }
            """)
        self.right_panel_layout = QGridLayout()
        self.right_panel.setLayout(self.right_panel_layout)

        self.layout.addWidget(
            self.left_panel,
            0, 0
        )
        self.layout.addWidget(
            self.right_panel,
            0, 1
        )

        # Building left panel elements
        self.build_parameters()

        self.mob_button = QPushButton("Générer le monstre")
        self.mob_button.clicked.connect(self.build_mob)
        self.left_panel_layout.addWidget(
            self.mob_button,
            5, 0,
            1, 1
        )

        self.save = QPushButton("Sauvegarder le monstre")
        self.save.clicked.connect(self.save_mob)
        self.left_panel_layout.addWidget(
            self.save,
            5, 1,
            1, 1
        )

        # Building right panel elements
        self.build_mob(True)

    def build_parameters(self):
        label = QLabel("<h1>Créé ton monstre !</h1>")
        self.left_panel_layout.addWidget(
            label,
            0, 0,
            1, 2
        )
        label.setAlignment(Qt.AlignCenter)
        label.setMaximumHeight(50)

        # Mob name
        self.left_panel_layout.addWidget(
            QLabel("Nom du monstre :"),
            1, 0
        )
        self.name = QLineEdit()
        self.left_panel_layout.addWidget(
            self.name,
            1, 1
        )

        # Floor
        self.left_panel_layout.addWidget(
            QLabel("Étage d'origine :"),
            2, 0
        )
        self.box_floor = QComboBox()
        for key, value in LEVEL.items():
            self.box_floor.addItem(key, value)

        self.left_panel_layout.addWidget(
            self.box_floor,
            2, 1
        )

        # Base
        self.left_panel_layout.addWidget(
            QLabel("Type de monstre :"),
            3, 0
        )
        self.box_type = QComboBox()
        for key, value in MOB_TYPE.items():
            self.box_type.addItem(key, value)
        self.left_panel_layout.addWidget(
            self.box_type,
            3, 1
        )

        # main stat
        self.left_panel_layout.addWidget(
            QLabel("Carac principale :"),
            4, 0
        )
        self.box_stat = QComboBox()
        for key, value in STATS.items():
            self.box_stat.addItem(key, value)
        self.left_panel_layout.addWidget(
            self.box_stat,
            4, 1
        )

    def build_mob(
            self,
            default: bool = False
    ):
        if default:
            default_mob = Mob(name="Example mob", level=5, power=5, main_stat="Perception")
            self.mob_sheet = QSheet(default_mob)
            self.right_panel_layout.addWidget(
                self.mob_sheet,
                1, 2,
                self.right_panel_layout.rowCount(), 1
            )
            return

        dict_param = {
            "name": self.name.text(),
            "level": self.box_floor.currentData(),
            "power": self.box_type.currentData(),
            "main_stat": self.box_stat.currentText()
        }

        self.mob = Mob(**dict_param)
        if self.mob_sheet is not None:
            self.right_panel_layout.removeWidget(self.mob_sheet)
            self.mob_sheet.deleteLater()
        self.mob_sheet = QSheet(self.mob)
        self.right_panel_layout.addWidget(
            self.mob_sheet,
            1, 2,
            self.right_panel_layout.rowCount(), 1
        )

    def save_mob(self):
        self.mob.save_mob()


def launch_app():
    app = QApplication(sys.argv)
    fenetre = MaFenetre()
    fenetre.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        fenetre = MaFenetre()
        fenetre.show()

        sys.exit(app.exec_())
    except Exception as e:
        input(f"There was an error: {e}")
