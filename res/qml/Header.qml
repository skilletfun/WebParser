import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    color: 'transparent'

// ---------------------  Title ----------------------- //
    Text {
        id: title

        text: 'WebParser ' + parser.get_version()
        font.pixelSize: 32
        font.bold: true
        font.family: 'Arial'

        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 45
        anchors.topMargin: 30
    }

// ---------------------  Author - Skilletfun ----------------------- //
    Text {
        id: author
        visible: false
        text: 'by Skilletfun'
        font.pixelSize: 25
        font.italic: true
        font.family: 'Calibri'

        anchors.right: parent.right
        anchors.rightMargin: 45
        anchors.verticalCenter: title.verticalCenter
    }

// ---------------------  Supported sites ----------------------- //
    Text {
        id: help_title

        text: 'Support 16 sites'
        font.pixelSize: 16
        font.family: 'Arial'

        anchors.left: parent.left
        anchors.top: title.bottom
        anchors.leftMargin: 45
        anchors.topMargin: 10
    }

// ---------------------  Help button that open list of sites ----------------------- //
    Button {
        id: help_title_btn

        height: 20
        width: height

        background: Rectangle { radius: height/2; border.color: 'black';
            color: help_title_btn.pressed ? color_press : help_title_btn.hovered ? color_hover : 'white'; }

        anchors.verticalCenter: help_title.verticalCenter
        anchors.left: help_title.right
        anchors.leftMargin: 20

        text: '?'

        onReleased: {
            help_title_popup.open();
        }
    }

// ---------------------  Popup with list of sites ----------------------- //
    Popup {
        id: help_title_popup

        width: parent.width/3
        height: parent.height / 1.2

        background: Rectangle { border.color: "black"; radius: 15 }

        modal: true

        enter: Transition {
            NumberAnimation { property: 'opacity'; from: 0; to: 1; duration: 200 }
        }

        exit: Transition {
            NumberAnimation { property: 'opacity'; from: 1; to: 0; duration: 200 }
        }

        anchors.centerIn: parent

        ListView {
            id: list_sites

            clip: true
            model: model_sites
            
            ScrollBar.vertical: ScrollBar {
                active: true;
                onActiveChanged: { if (!active) active = true; }
            }

            headerPositioning: ListView.OverlayHeader
            header: Rectangle {
                z: 2
                clip: true
                height: 30
                width: parent.width

                Text {
                    text: '-   ©  -  required chromedriver   -'
                    anchors.top: parent.top
                    anchors.horizontalCenter: parent.horizontalCenter
                    font.pixelSize: 16
                    font.family: 'Arial'
                }
            }

            anchors.fill: parent
            anchors.margins: 5
            spacing: 15

            delegate: Text {
                text: _text
                font.pixelSize: 16
                font.family: 'Arial'
            }
        }

        ListModel {
            id: model_sites

            Component.onCompleted: {
                var arr = ['© ac.qq.com', '© bomtoon.com (+ paid)', 'comic.naver.com', '© comico.kr (+ paid)', '© fanfox.net',
                           '© kuaikanmanhua.com', '© manga.bilibili.com', 'mangakakalots.com', '© mangareader.to',
                           'manhuadb.com', 'scansnelo.com', '© page.kakao.com (+ paid)', 'rawdevart.com', '© ridibooks.com (+ paid)',
			               'webmota.com (baozihm.com)', 'webtoons.com'];
                arr.forEach(function(el){ append({ '_text': el }); });
            }
        }
    }
}
