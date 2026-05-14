from PyQt6.QtWidgets import QStackedWidget, QGraphicsOpacityEffect
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QPoint


class AnimatedRouter(QStackedWidget):
    """
    Drop-in QStackedWidget replacement that plays a combined
    fade + horizontal-slide transition between pages.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._duration = 350
        self._easing   = QEasingCurve.Type.InOutCubic
        self._animating = False

    def switch_to(self, index: int):
        if index == self.currentIndex() or self._animating:
            return

        new_widget = self.widget(index)
        if new_widget is None:
            return

        forward = index > self.currentIndex()
        self._animating = True

        # ── opacity ──────────────────────────────────────────────────────────
        effect = QGraphicsOpacityEffect(new_widget)
        new_widget.setGraphicsEffect(effect)

        fade = QPropertyAnimation(effect, b"opacity")
        fade.setDuration(self._duration)
        fade.setStartValue(0.0)
        fade.setEndValue(1.0)
        fade.setEasingCurve(self._easing)

        # ── slide ─────────────────────────────────────────────────────────────
        offset = 40 if forward else -40
        slide = QPropertyAnimation(new_widget, b"pos")
        slide.setDuration(self._duration)
        slide.setStartValue(QPoint(offset, 0))
        slide.setEndValue(QPoint(0, 0))
        slide.setEasingCurve(self._easing)

        # ── group ─────────────────────────────────────────────────────────────
        self._group = QParallelAnimationGroup()
        self._group.addAnimation(fade)
        self._group.addAnimation(slide)
        self._group.finished.connect(lambda: self._on_done(new_widget))

        self.setCurrentIndex(index)
        self._group.start()

    def _on_done(self, widget):
        widget.setGraphicsEffect(None)   # clean up
        self._animating = False
