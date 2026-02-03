import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart'; // חובה עבור ה-Override

void main() {
  // עוקף את זיהוי המערכת לפלטפורמה ניטרלית למניעת קריסות בטסטים
  debugDefaultTargetPlatformOverride = TargetPlatform.fuchsia;

  runApp(const FletApp(
    pageUrl: String.fromEnvironment("FLET_TEST_APP_URL"),
    assetsDir: String.fromEnvironment("FLET_TEST_ASSETS_DIR"),
  ));
}