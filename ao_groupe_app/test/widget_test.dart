import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:ao_groupe_app/main.dart';

void main() {
  testWidgets('shows Arabic design-system preview with RTL direction', (
    tester,
  ) async {
    await tester.pumpWidget(const AoGroupeApp());
    await tester.pumpAndSettle();

    expect(find.text('AO groupe'), findsOneWidget);
    expect(find.text('معاينة نظام التصميم'), findsOneWidget);
    expect(find.text('نفد المخزون'), findsOneWidget);
    expect(
      Directionality.of(tester.element(find.text('معاينة نظام التصميم'))),
      TextDirection.rtl,
    );
  });

  testWidgets('switches the preview language to French', (tester) async {
    await tester.pumpWidget(const AoGroupeApp());
    await tester.pumpAndSettle();

    await tester.tap(find.byType(DropdownButton<Locale>));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Français').last);
    await tester.pumpAndSettle();

    expect(find.text('Aperçu du système de design'), findsOneWidget);
    expect(
      Directionality.of(
        tester.element(find.text('Aperçu du système de design')),
      ),
      TextDirection.ltr,
    );
  });

  testWidgets('switches between light and dark appearance', (tester) async {
    await tester.pumpWidget(const AoGroupeApp());
    await tester.pumpAndSettle();

    await tester.tap(find.text('داكن'));
    await tester.pumpAndSettle();
    expect(
      Theme.of(tester.element(find.text('معاينة نظام التصميم'))).brightness,
      Brightness.dark,
    );

    await tester.tap(find.text('فاتح'));
    await tester.pumpAndSettle();
    expect(
      Theme.of(tester.element(find.text('معاينة نظام التصميم'))).brightness,
      Brightness.light,
    );
  });
}
