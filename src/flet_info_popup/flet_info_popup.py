from enum import Enum
from typing import Any, Optional, Union
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.types import (
    ColorValue,
    OptionalControlEventCallable,
    ColorEnums,
    PaddingValue
)


class PopupDismissTriggerBehavior(Enum):
    """
    Popup dismiss trigger behavior enum.
    """
    ON_TAP_AREA = "on_tap_area"
    MANUAL = "manual"


class PopupPosition(Enum):
    """
    Popup position relative to the trigger control.
    """
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"


class FletInfoPopup(ConstrainedControl):
    """
    A custom popup widget with highlight support
    """

    def __init__(
        self,
        #
        # ConstrainedControl
        #
        ref=None,
        key=None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[dict] = None,
        opacity: OptionalNumber = None,
        rotate: Optional[dict] = None,
        scale: Optional[dict] = None,
        offset: Optional[dict] = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: Optional[dict] = None,
        animate_size: Optional[dict] = None,
        animate_position: Optional[dict] = None,
        animate_rotation: Optional[dict] = None,
        animate_scale: Optional[dict] = None,
        animate_offset: Optional[dict] = None,
        on_animation_end=None,
        tooltip: Optional[str] = None,
        badge: Optional[dict] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        rtl: Optional[bool] = None,
        #
        # FletInfoPopup specific
        #
        content: Optional[Control] = None,
        body: Optional[Control] = None,
        dismiss_trigger_behavior: Optional[PopupDismissTriggerBehavior] = PopupDismissTriggerBehavior.ON_TAP_AREA,
        popup_position: Optional[PopupPosition] = PopupPosition.BOTTOM,
        area_background_color: Optional[ColorValue] = None,
        enable_highlight: Optional[bool] = None,
        highlight_background_color: Optional[ColorValue] = None,
        highlight_border_radius: OptionalNumber = None,
        highlight_padding: Optional[PaddingValue] = None,
        on_controller_created: OptionalControlEventCallable = None,
        on_area_pressed: OptionalControlEventCallable = None,
        on_dismissed: OptionalControlEventCallable = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
            rtl=rtl,
        )

        # Initialize private attributes
        self.__content = None
        self.__body = None
        self.__dismiss_trigger_behavior = None
        self.__popup_position = None
        self.__area_background_color = None
        self.__highlight_background_color = None

        # Set properties through setters
        self.content = content
        self.body = body
        self.dismiss_trigger_behavior = dismiss_trigger_behavior
        self.popup_position = popup_position
        self.area_background_color = area_background_color
        self.enable_highlight = enable_highlight
        self.highlight_background_color = highlight_background_color
        self.highlight_border_radius = highlight_border_radius
        self.highlight_padding = highlight_padding
        self.on_controller_created = on_controller_created
        self.on_area_pressed = on_area_pressed
        self.on_dismissed = on_dismissed

    def _get_control_name(self):
        return "flet_info_popup"

    def _get_children(self):
        children = []
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        if self.__body is not None:
            self.__body._set_attr_internal("n", "body")
            children.append(self.__body)
        return children

    # content - the trigger control
    @property
    def content(self) -> Optional[Control]:
        """
        The control that triggers the popup when interacted with.
        """
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # body - the popup content
    @property
    def body(self) -> Optional[Control]:
        """
        The custom content to display inside the popup.
        """
        return self.__body

    @body.setter
    def body(self, value: Optional[Control]):
        self.__body = value

    # dismiss_trigger_behavior
    @property
    def dismiss_trigger_behavior(self) -> Optional[PopupDismissTriggerBehavior]:
        """
        The behavior that triggers dismissing the popup.
        """
        return self.__dismiss_trigger_behavior

    @dismiss_trigger_behavior.setter
    def dismiss_trigger_behavior(self, value: Optional[PopupDismissTriggerBehavior]):
        self.__dismiss_trigger_behavior = value
        self._set_attr("dismissTriggerBehavior", value.value if value else None)

    # popup_position
    @property
    def popup_position(self) -> Optional[PopupPosition]:
        """
        The position of the popup relative to the trigger control.
        """
        return self.__popup_position

    @popup_position.setter
    def popup_position(self, value: Optional[PopupPosition]):
        self.__popup_position = value
        self._set_attr("popupPosition", value.value if value else None)

    # area_background_color
    @property
    def area_background_color(self) -> Optional[ColorValue]:
        """
        The background color of the area outside the popup.
        """
        return self.__area_background_color

    @area_background_color.setter
    def area_background_color(self, value: Optional[ColorValue]):
        self.__area_background_color = value
        self._set_enum_attr("areaBackgroundColor", value, ColorEnums)

    # enable_highlight
    @property
    def enable_highlight(self) -> Optional[bool]:
        """
        Whether to enable highlighting of the trigger control.
        """
        return self._get_attr("enableHighlight", data_type="bool")

    @enable_highlight.setter
    def enable_highlight(self, value: Optional[bool]):
        self._set_attr("enableHighlight", value)

    # highlight_background_color
    @property
    def highlight_background_color(self) -> Optional[ColorValue]:
        """
        The background color of the highlight area.
        """
        return self.__highlight_background_color

    @highlight_background_color.setter
    def highlight_background_color(self, value: Optional[ColorValue]):
        self.__highlight_background_color = value
        self._set_enum_attr("highlightBackgroundColor", value, ColorEnums)

    # highlight_border_radius
    @property
    def highlight_border_radius(self) -> OptionalNumber:
        """
        The border radius of the highlight area.
        """
        return self._get_attr("highlightBorderRadius", data_type="float")

    @highlight_border_radius.setter
    def highlight_border_radius(self, value: OptionalNumber):
        self._set_attr("highlightBorderRadius", value)

    # highlight_padding
    @property
    def highlight_padding(self) -> Optional[PaddingValue]:
        """
        The padding of the highlight area. Can be a single number or padding object.
        """
        return self._get_attr("highlightPadding")

    @highlight_padding.setter
    def highlight_padding(self, value: Optional[PaddingValue]):
        self._set_attr("highlightPadding", value)

    # Event handlers
    @property
    def on_controller_created(self) -> OptionalControlEventCallable:
        """
        Event handler called when the popup controller is created.
        """
        return self._get_event_handler("controller_created")

    @on_controller_created.setter
    def on_controller_created(self, handler: OptionalControlEventCallable):
        self._add_event_handler("controller_created", handler)

    @property
    def on_area_pressed(self) -> OptionalControlEventCallable:
        """
        Event handler called when the area outside the popup is pressed.
        """
        return self._get_event_handler("area_pressed")

    @on_area_pressed.setter
    def on_area_pressed(self, handler: OptionalControlEventCallable):
        self._add_event_handler("area_pressed", handler)

    @property
    def on_dismissed(self) -> OptionalControlEventCallable:
        """
        Event handler called when the popup is dismissed.
        """
        return self._get_event_handler("dismissed")

    @on_dismissed.setter
    def on_dismissed(self, handler: OptionalControlEventCallable):
        self._add_event_handler("dismissed", handler)

    # Methods
    def show(self):
        """
        Show the popup programmatically.
        """
        self.invoke_method("show", wait_for_result=False)

    def hide(self):
        """
        Hide the popup programmatically.
        """
        self.invoke_method("hide", wait_for_result=False)

    def dismiss(self):
        """
        Dismiss the popup programmatically. Alias for hide().
        """
        self.hide()

    def open(self):
        """
        Open the popup programmatically. Alias for show().
        """
        self.show()

    def close(self):
        """
        Close the popup programmatically. Alias for hide().
        """
        self.hide()
