import QtQuick 2.15
import QtQuick.Controls 2.15
import Qt.labs.platform 1.0


Rectangle {
    id: chapter_settings_rect

    property string folder: chooseSaveFolderDialog.folder
    property string url: url_field.text
    property string count_of_chapters: chapter_count_field.text

    width: 575
    height: 300
    radius: 30
    border.color: "black"

    // Title

    Text {
        id: title_chapter_settings
        text: 'Chapter settings'
        font.family: 'Arial'
        font.pixelSize: 18
        font.italic: true
        y: 20
        anchors.horizontalCenter: parent.horizontalCenter
    }

    // Label Url

    Text {
        id: chapter_url_text
        text: 'Url'
        font.family: 'Arial'
        font.pixelSize: 16
        x: 45
        anchors.top: title_chapter_settings.top
        anchors.topMargin: 40
    }

    // Url Field

    TextField {
        id: url_field

        anchors.left: chapter_url_text.left
        anchors.top: chapter_url_text.bottom
        anchors.topMargin: 10

        height: 50
        width: 420

        selectionColor: color_select

        background: Rectangle { radius: 10; border.width: 1;
            color: url_field.focus ? color_press : url_field.hovered ? color_hover : 'white'; }

        placeholderText: "https://somesite.com/title/chapter/12"
        font.pixelSize: 18

        onAccepted: { focus = false; }

        onEditingFinished: { focus = false; }
    }

    // Button open file with urls

    Button {
        id: btn_urls

        height: url_field.height
        width: height

        anchors.left: url_field.right
        anchors.verticalCenter: url_field.verticalCenter
        anchors.leftMargin: 15

        icon.source: '../icons/openurls.png'
        icon.color: 'transparent'
        icon.width: width * 0.9
        icon.height: width * 0.9

        background: Rectangle { color: btn_urls.down ? color_press : btn_urls.hovered ? color_hover : 'white'; }

        onReleased: { urls_file_dialog.open(); }
    }

    FileDialog {
        id: urls_file_dialog
        title: 'Choose file with urls'
        onAccepted: { url_field.text = file; }
    }

    // Label count of chapters

    Text {
        id: chapter_count_text

        text: 'Count of chapters\n' + '* for all available'
        font.family: 'Arial'
        font.pixelSize: 16

        anchors.left: chapter_url_text.left
        anchors.top: url_field.bottom
        anchors.topMargin: 40
    }

    // Field with count of chapters

    TextField {
        id: chapter_count_field

        width: 70
        height: 50

        validator: RegExpValidator { regExp: /[0-9*]+/ }

        horizontalAlignment: Text.AlignHCenter

        anchors.left: chapter_url_text.left
        anchors.top: chapter_count_text.bottom
        anchors.topMargin: 10

        selectionColor: color_select
        background: Rectangle { radius: 10; border.width: 1;
            color: chapter_count_field.focus ? color_press : chapter_count_field.hovered ? color_hover : 'white'; }

        placeholderText: "1"
        font.pixelSize: 18

        onAccepted: { focus = false; }

        onEditingFinished: { focus = false; }
    }

    // Button save folder

    Button {
        id: chooseSaveFolder

        height: chapter_count_field.height
        width: height

        icon.source: '../icons/savefolder.png'
        icon.color: 'transparent'
        icon.width: width * 0.9
        icon.height: width * 0.9

        anchors.verticalCenter: chapter_count_field.verticalCenter
        anchors.left: btn_urls.left

        background: Rectangle { color: chooseSaveFolder.down ? color_press : chooseSaveFolder.hovered ? color_hover : 'white'; }

        onReleased: { chooseSaveFolderDialog.open(); }
    }

    FolderDialog {
        id: chooseSaveFolderDialog
        title: "Choose save folder"
    }
}
