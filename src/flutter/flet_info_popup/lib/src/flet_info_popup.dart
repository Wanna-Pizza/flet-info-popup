import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

class _HighlightClipper extends CustomClipper<Path> {
  final Rect targetRect;
  final BorderRadius borderRadius;
  final EdgeInsets padding;

  _HighlightClipper({
    required this.targetRect,
    required this.borderRadius,
    required this.padding,
  });

  @override
  Path getClip(Size size) {
    final highlightRect = Rect.fromLTRB(
      targetRect.left - padding.left,
      targetRect.top - padding.top,
      targetRect.right + padding.right,
      targetRect.bottom + padding.bottom,
    );

    return Path()
      ..fillType = PathFillType.evenOdd
      ..addRect(Offset.zero & size)
      ..addRRect(
        RRect.fromRectAndCorners(
          highlightRect,
          topLeft: borderRadius.topLeft,
          topRight: borderRadius.topRight,
          bottomLeft: borderRadius.bottomLeft,
          bottomRight: borderRadius.bottomRight,
        ),
      );
  }

  @override
  bool shouldReclip(_HighlightClipper oldClipper) =>
      targetRect != oldClipper.targetRect ||
      borderRadius != oldClipper.borderRadius ||
      padding != oldClipper.padding;
}

class FletInfoPopupControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend? backend;

  const FletInfoPopupControl({
    super.key,
    required this.parent,
    required this.control,
    required this.children,
    required this.parentDisabled,
    required this.parentAdaptive,
    required this.backend,
  });

  @override
  State<FletInfoPopupControl> createState() => _FletInfoPopupControlState();
}

class _FletInfoPopupControlState extends State<FletInfoPopupControl> with SingleTickerProviderStateMixin {
  OverlayEntry? _overlayEntry;
  final GlobalKey _contentKey = GlobalKey();
  final LayerLink _layerLink = LayerLink();
  late AnimationController _animationController;
  late Animation<double> _opacityAnimation;
  late Animation<Offset> _positionAnimation;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 300),
      vsync: this,
    );
    
    _opacityAnimation = CurvedAnimation(
      parent: _animationController,
      curve: Curves.linearToEaseOut,
    );
    
    _positionAnimation = Tween<Offset>(
      begin: const Offset(0, 0.1),
      end: Offset.zero,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.linearToEaseOut,
    ));
    
    if (widget.backend != null) {
      widget.backend!.subscribeMethods(widget.control.id, _onMethodCall);
    }
  }

  @override
  void dispose() {
    _animationController.dispose();
    if (widget.backend != null) {
      widget.backend!.unsubscribeMethods(widget.control.id);
    }
    super.dispose();
  }

  Future<String?> _onMethodCall(
      String methodName, Map<String, String> args) async {
    switch (methodName) {
      case "show":
      case "open":
        _showOverlay();
        return null;
      case "hide":
      case "close":
      case "dismiss":
        _hideOverlay();
        return null;
      default:
        return null;
    }
  }

  void _showOverlay() {
    if (_overlayEntry != null) return;

    final renderBox = _contentKey.currentContext?.findRenderObject() as RenderBox?;
    if (renderBox == null) return;

    _overlayEntry = OverlayEntry(
      builder: (context) => _buildOverlay(renderBox),
    );

    Overlay.of(context).insert(_overlayEntry!);
    
    _animationController.forward();

    if (widget.backend != null) {
      widget.backend!.triggerControlEvent(widget.control.id, "controller_created", "");
    }
  }

  void _hideOverlay() {
    _animationController.reverse().then((_) {
      _overlayEntry?.remove();
      _overlayEntry = null;

      if (widget.backend != null) {
        widget.backend!.triggerControlEvent(widget.control.id, "dismissed", "");
      }
    });
  }

  Widget _buildOverlay(RenderBox targetRenderBox) {
    var bodyControls = widget.children.where((c) => c.name == "body" && c.isVisible);
    bool? adaptive = widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    // Parse settings
    bool enableHighlight = widget.control.attrBool("enableHighlight", false)!;
    Color? highlightBackgroundColor = widget.control.attrColor("highlightBackgroundColor", context);
    Color? areaBackgroundColor = widget.control.attrColor("areaBackgroundColor", context);
    
    double highlightBorderRadius = widget.control.attrDouble("highlightBorderRadius", 8.0)!;
    
    // Parse highlight padding
    var highlightPadding = parseEdgeInsets(widget.control, "highlightPadding") ?? const EdgeInsets.all(8.0);
    
    String? dismissBehavior = widget.control.attrString("dismissTriggerBehavior", "onTapArea");
    bool dismissOnTapOutside = dismissBehavior != "manual" && dismissBehavior != "manuel";

    String? position = widget.control.attrString("popupPosition", "bottom");

    // Get target position
    final targetPosition = targetRenderBox.localToGlobal(Offset.zero);
    final targetSize = targetRenderBox.size;
    final targetRect = targetPosition & targetSize;

    // Calculate popup position based on position parameter
    double? popupLeft;
    double? popupTop;
    double? popupRight;
    double? popupBottom;
    const double spacing = 10.0;

    switch (position) {
      case "top":
        popupLeft = targetPosition.dx;
        popupBottom = MediaQuery.of(context).size.height - targetPosition.dy + spacing;
        break;
      case "bottom":
        popupLeft = targetPosition.dx;
        popupTop = targetPosition.dy + targetSize.height + spacing;
        break;
      case "left":
        popupRight = MediaQuery.of(context).size.width - targetPosition.dx + spacing;
        popupTop = targetPosition.dy;
        break;
      case "right":
        popupLeft = targetPosition.dx + targetSize.width + spacing;
        popupTop = targetPosition.dy;
        break;
      case "top_left":
        popupRight = MediaQuery.of(context).size.width - targetPosition.dx + spacing;
        popupBottom = MediaQuery.of(context).size.height - targetPosition.dy + spacing;
        break;
      case "top_right":
        popupLeft = targetPosition.dx + targetSize.width + spacing;
        popupBottom = MediaQuery.of(context).size.height - targetPosition.dy + spacing;
        break;
      case "bottom_left":
        popupRight = MediaQuery.of(context).size.width - targetPosition.dx + spacing;
        popupTop = targetPosition.dy + targetSize.height + spacing;
        break;
      case "bottom_right":
        popupLeft = targetPosition.dx + targetSize.width + spacing;
        popupTop = targetPosition.dy + targetSize.height + spacing;
        break;
      default: // bottom
        popupLeft = targetPosition.dx;
        popupTop = targetPosition.dy + targetSize.height + spacing;
    }

    return AnimatedBuilder(
      animation: _animationController,
      builder: (context, child) {
        return Opacity(
          opacity: _opacityAnimation.value,
          child: GestureDetector(
            onTap: dismissOnTapOutside
                ? () {
                    _hideOverlay();
                    if (widget.backend != null) {
                      widget.backend!.triggerControlEvent(widget.control.id, "area_pressed", "");
                    }
                  }
                : null,
            child: Material(
              color: Colors.transparent,
              child: Stack(
                children: [
                  if (enableHighlight)
                    ClipPath(
                      clipper: _HighlightClipper(
                        targetRect: targetRect,
                        borderRadius: BorderRadius.circular(highlightBorderRadius),
                        padding: highlightPadding,
                      ),
                      child: Container(
                        width: double.infinity,
                        height: double.infinity,
                        color: highlightBackgroundColor ?? Colors.black.withOpacity(0.7),
                      ),
                    )
                  else
                    Container(
                      width: double.infinity,
                      height: double.infinity,
                      color: areaBackgroundColor ?? Colors.transparent,
                    ),

                  Positioned(
                    left: popupLeft,
                    top: popupTop,
                    right: popupRight,
                    bottom: popupBottom,
                    child: SlideTransition(
                      position: _positionAnimation,
                      child: Material(
                        color: Colors.transparent,
                        child: bodyControls.isNotEmpty
                            ? createControl(
                                widget.control,
                                bodyControls.first.id,
                                disabled,
                                parentAdaptive: adaptive,
                              )
                            : const SizedBox.shrink(),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    var contentControls = widget.children.where((c) => c.name == "content" && c.isVisible);
    
    bool? adaptive = widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    Widget contentWidget = contentControls.isNotEmpty
        ? CompositedTransformTarget(
            link: _layerLink,
            key: _contentKey,
            child: createControl(
              widget.control,
              contentControls.first.id,
              disabled,
              parentAdaptive: adaptive,
            ),
          )
        : const SizedBox.shrink();

    return constrainedControl(context, contentWidget, widget.parent, widget.control);
  }
}
