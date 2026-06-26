Attribute VB_Name = "OptionalPagesRibbon"
Option Explicit

' =========================================================
' Abs. prace - vlastni karta Wordu
' Detekce stavu vyhradne pres zalozky vlozene do kp-app.dotx
' (build_dotx_blocks.py): OPT_BLANK_FRONT, OPT_BLANK_BACK, OPT_THANKS,
' OPT_THANKS_ANCHOR. Zadne krehke heuristiky (hledani zalomu, "posledni
' sekce prazdna", pocitani odstavcu) - ty drive zpusobovaly zaseknuti.
'
'   - Prazdne okolo: prazdna strana na zacatku (rucni zalom v necislovane
'     uvodni sekci) + prazdna strana na konci (terminalni oddil, bez cisla -
'     footer3.xml nema pole PAGE). Zadni se neMAZE: prepina se SectionStart
'     (nextPage/continuous) + Footer.LinkToPrevious, takze se nedotyka
'     koncove odstavcove znacky dokumentu.
'   - Podekovani: zalom za podpisem zustava natvrdo; blok (odskok 567 b. ve
'     stylu Zakladni text + text + koncovy zalom) se maze/obnovuje na kotve
'     OPT_THANKS_ANCHOR. Obsah je tak vzdy na vlastni strance.
'
' Texty s diakritikou se sestavuji pres ChrW (literaly s diakritikou se pri
' importu .bas na macOS rozbijeji).
' =========================================================

Private Const BM_BLANK_FRONT As String = "OPT_BLANK_FRONT"
Private Const BM_BLANK_BACK As String = "OPT_BLANK_BACK"
Private Const BM_THANKS As String = "OPT_THANKS"
Private Const BM_THANKS_ANCHOR As String = "OPT_THANKS_ANCHOR"

Private Const WD_PAGE_BREAK As Long = 7
Private Const WD_SECTION_NEW_PAGE As Long = 2
Private Const WD_SECTION_CONTINUOUS As Long = 0

Private Const THANKS_SPACER_POINTS As Single = 567

Private rbn As IRibbonUI

' =========================================================
' Ribbon callbacks (signatury presne dle Microsoft dokumentace:
' button = control As IRibbonControl; toggleButton onAction =
' control As IRibbonControl, pressed As Boolean)
' =========================================================

Public Sub Ribbon_OnLoad(ribbon As IRibbonUI)
    Set rbn = ribbon
End Sub

Public Sub Ribbon_GetPressed_PrazdneOkolo(control As IRibbonControl, ByRef pressed)
    pressed = FrontBlankPresent() Or BackBlankPresent()
End Sub

Public Sub Ribbon_GetPressed_Podekovani(control As IRibbonControl, ByRef pressed)
    pressed = PodekovaniPresent()
End Sub

Public Sub Ribbon_TogglePrazdneOkolo(control As IRibbonControl, pressed As Boolean)
    TogglePrazdneOkolo
End Sub

Public Sub Ribbon_TogglePodekovani(control As IRibbonControl, pressed As Boolean)
    TogglePodekovani
End Sub

Public Sub Ribbon_AktualizovatPole(control As IRibbonControl)
    AktualizovatPoleVDokumentu
End Sub

Public Sub Ribbon_InfoVolitelneStranky(control As IRibbonControl)
    MsgBox "Abs. prace - volitelne bloky:" & vbCrLf & vbCrLf & _
           "Prazdne okolo = prazdna strana na zacatku i na konci dokumentu." & vbCrLf & _
           "Podekovani = strana s podekovanim pred Obsahem." & vbCrLf & vbCrLf & _
           "Obe tlacitka jsou ve vychozim stavu zmacknuta, protoze sablona " & _
           "tyto casti uz obsahuje.", _
           vbInformation, "Abs. prace"
End Sub

' =========================================================
' Verejna makra spustitelna i pres Alt+F8
' =========================================================

Public Sub TogglePrazdneOkolo()
    On Error GoTo ErrHandler

    Application.ScreenUpdating = False

    If FrontBlankPresent() Or BackBlankPresent() Then
        RemoveFrontBlank
        RemoveBackBlank
    Else
        InsertBackBlank
        InsertFrontBlank
    End If

    AktualizovatPoleVDokumentu

CleanExit:
    Application.ScreenUpdating = True
    On Error Resume Next
    If Not (rbn Is Nothing) Then rbn.InvalidateControl "btnPrazdneOkolo"
    On Error GoTo 0
    Exit Sub

ErrHandler:
    Application.ScreenUpdating = True
    MsgBox "Chyba v TogglePrazdneOkolo: " & Err.Description, vbExclamation, "Abs. prace"
End Sub

Public Sub TogglePodekovani()
    On Error GoTo ErrHandler

    Application.ScreenUpdating = False

    If PodekovaniPresent() Then
        RemovePodekovani
    Else
        InsertPodekovani
    End If

    AktualizovatPoleVDokumentu

CleanExit:
    Application.ScreenUpdating = True
    On Error Resume Next
    If Not (rbn Is Nothing) Then rbn.InvalidateControl "btnPodekovani"
    On Error GoTo 0
    Exit Sub

ErrHandler:
    Application.ScreenUpdating = True
    MsgBox "Chyba v TogglePodekovani: " & Err.Description, vbExclamation, "Abs. prace"
End Sub

' =========================================================
' Predni prazdna strana (rucni zalom v uvodni necislovane sekci)
' =========================================================

Private Function FrontBlankPresent() As Boolean
    FrontBlankPresent = ActiveDocument.Bookmarks.Exists(BM_BLANK_FRONT)
End Function

Private Sub RemoveFrontBlank()
    If FrontBlankPresent() Then ActiveDocument.Bookmarks(BM_BLANK_FRONT).Range.Delete
End Sub

Private Sub InsertFrontBlank()
    Dim doc As Document
    Dim rng As Range
    Dim rngBreak As Range

    Set doc = ActiveDocument
    If FrontBlankPresent() Then Exit Sub

    ' Prazdny uvodni odstavec + rucni zalom stranky.
    Set rng = doc.Range(0, 0)
    rng.Text = vbCr

    Set rngBreak = doc.Range(1, 1)
    rngBreak.InsertBreak Type:=WD_PAGE_BREAK

    doc.Bookmarks.Add BM_BLANK_FRONT, doc.Range(0, rngBreak.End)
End Sub

' =========================================================
' Zadni prazdna strana (terminalni oddil - prepinani SectionStart,
' bez mazani koncove odstavcove znacky)
' =========================================================

Private Function BackBlankPresent() As Boolean
    BackBlankPresent = ActiveDocument.Bookmarks.Exists(BM_BLANK_BACK)
End Function

Private Sub RemoveBackBlank()
    Dim doc As Document
    Dim sec As Section
    Dim i As Long

    Set doc = ActiveDocument
    If Not BackBlankPresent() Then Exit Sub

    Set sec = doc.Sections(doc.Sections.Count)
    sec.PageSetup.SectionStart = WD_SECTION_CONTINUOUS

    ' Sdilena strana ma zase nest cislo predchozi sekce.
    For i = 1 To 3
        sec.Footers(i).LinkToPrevious = True
    Next i

    doc.Bookmarks(BM_BLANK_BACK).Delete
End Sub

Private Sub InsertBackBlank()
    Dim doc As Document
    Dim sec As Section

    Set doc = ActiveDocument
    If BackBlankPresent() Then Exit Sub

    Set sec = doc.Sections(doc.Sections.Count)
    sec.PageSetup.SectionStart = WD_SECTION_NEW_PAGE
    ClearSectionHeadersFooters sec

    doc.Bookmarks.Add BM_BLANK_BACK, sec.Range
End Sub

' =========================================================
' Podekovani (blok na kotve OPT_THANKS_ANCHOR pred Obsahem)
' =========================================================

Private Function PodekovaniPresent() As Boolean
    PodekovaniPresent = ActiveDocument.Bookmarks.Exists(BM_THANKS)
End Function

Private Sub RemovePodekovani()
    If PodekovaniPresent() Then ActiveDocument.Bookmarks(BM_THANKS).Range.Delete
End Sub

Private Sub InsertPodekovani()
    Dim doc As Document
    Dim rng As Range
    Dim rngBreak As Range
    Dim startPos As Long

    Set doc = ActiveDocument
    If PodekovaniPresent() Then Exit Sub
    If Not doc.Bookmarks.Exists(BM_THANKS_ANCHOR) Then Exit Sub

    startPos = doc.Bookmarks(BM_THANKS_ANCHOR).Range.Start

    ' Odskok (prazdny odstavec, 567 b. za) + text, oboji stylem Zakladni text.
    Set rng = doc.Range(startPos, startPos)
    rng.Text = vbCr & ThanksText() & vbCr
    rng.Style = StyleBase()
    rng.Paragraphs(1).SpaceAfter = THANKS_SPACER_POINTS

    ' Koncovy zalom stranky, aby Obsah zacinal na vlastni strance.
    Set rngBreak = doc.Range(rng.End, rng.End)
    rngBreak.InsertBreak Type:=WD_PAGE_BREAK

    ' Konec bloku = aktualni zacatek kotvy (obepina Obsah, posunula se o vlozeny
    ' obsah). Tim zalozka konci presne pred Obsahem a nezasahuje do kotvy.
    doc.Bookmarks.Add BM_THANKS, doc.Range(startPos, doc.Bookmarks(BM_THANKS_ANCHOR).Range.Start)
End Sub

' =========================================================
' Pomocne rutiny
' =========================================================

Private Function StyleBase() As String
    ' nazev stylu "Zakladni Text" s diakritikou: 225=a-carka, 237=i-carka
    StyleBase = "Z" & ChrW(225) & "kladn" & ChrW(237) & " Text"
End Function

Private Function ThanksText() As String
    ' "Text podekovani - nepovinne." s diakritikou:
    ' 283=e-hacek, 225=a-carka, 237=i-carka, 8211=dlouha pomlcka, 233=e-carka
    ThanksText = "Text pod" & ChrW(283) & "kov" & ChrW(225) & "n" & ChrW(237) _
        & " " & ChrW(8211) & " nepovinn" & ChrW(233) & "."
End Function

Private Sub ClearSectionHeadersFooters(ByVal sec As Section)
    Dim i As Long

    On Error Resume Next

    For i = 1 To 3
        sec.Headers(i).LinkToPrevious = False
        sec.Headers(i).Range.Text = ""
        sec.Footers(i).LinkToPrevious = False
        sec.Footers(i).Range.Text = ""
    Next i

    On Error GoTo 0
End Sub

Private Sub AktualizovatPoleVDokumentu()
    Dim story As Range
    Dim nextStory As Range

    On Error Resume Next

    For Each story In ActiveDocument.StoryRanges
        story.Fields.Update
        Set nextStory = story.NextStoryRange

        Do While Not (nextStory Is Nothing)
            nextStory.Fields.Update
            Set nextStory = nextStory.NextStoryRange
        Loop
    Next story

    On Error GoTo 0
End Sub
