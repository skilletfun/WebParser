import QtQuick 2.15
import QtQuick.Controls 2.15

Popup {
    property string redownload: redownload_images_field.text
    width: 600
    height: 150

    modal: true

    background: Rectangle { border.color: "black"; radius: 20 }

    enter: Transition {
        NumberAnimation { property: 'opacity'; from: 0; to: 1; duration: 200 }
    }

    exit: Transition {
        NumberAnimation { property: 'opacity'; from: 1; to: 0; duration: 200 }
    }

    Text {
        id: redownload_images_text

        text: 'Numbers images that should to redownload'
        font.family: 'Arial'
        font.pixelSize: 16

        x: 45
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.margins: 15
    }

    TextField {
        id: redownload_images_field

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: redownload_images_text.bottom
        anchors.margins: 15
        anchors.topMargin: 10
        height: 50

        selectionColor: color_select

        background: Rectangle { radius: 10; border.width: 1; color: redownload_images_field.focus ?
                color_press : redownload_images_field.hovered ? color_hover : 'white'; }

        placeholderText: '1 3 13'
        font.pixelSize: 18

        onAccepted: { focus = false; }

        onEditingFinished: { focus = false; }
    }
}
