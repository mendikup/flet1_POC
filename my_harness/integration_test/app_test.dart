import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:flet/flet.dart';

void main() {
  final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets("Flet App Test", (WidgetTester tester) async {
    // התאמה ל-Fuchsia וגודל מסך קבוע
    debugDefaultTargetPlatformOverride = TargetPlatform.fuchsia;
    await binding.setSurfaceSize(const Size(1280, 720));

    await tester.pumpWidget(const FletApp(
      pageUrl: String.fromEnvironment("FLET_TEST_APP_URL"),
      assetsDir: String.fromEnvironment("FLET_TEST_ASSETS_DIR"),
    ));

    // המתנה ארוכה לפעולות מהפייתון
    await Future.delayed(const Duration(minutes: 10));
  });
}