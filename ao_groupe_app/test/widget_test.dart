import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:ao_groupe_app/main.dart';

void main() {
  testWidgets('shows onboarding and opens the Arabic RTL storefront', (
    tester,
  ) async {
    SharedPreferences.setMockInitialValues({});
    await tester.pumpWidget(const AoGroupeApp());
    await tester.pump(const Duration(milliseconds: 800));
    await tester.pumpAndSettle();

    expect(find.text('أهلاً بك في AO groupe'), findsOneWidget);
    await tester.tap(find.text('تخطي'));
    await tester.pumpAndSettle();

    expect(find.text('AO groupe'), findsOneWidget);
    expect(find.text('كل حلول الكهرباء والطاقة، في مكان واحد'), findsOneWidget);
    expect(
      Directionality.of(
        tester.element(find.text('كل حلول الكهرباء والطاقة، في مكان واحد')),
      ),
      TextDirection.rtl,
    );
    final preferences = await SharedPreferences.getInstance();
    expect(preferences.getBool('onboarding.complete'), isTrue);
  });

  testWidgets('opens persisted onboarding directly to the storefront', (
    tester,
  ) async {
    SharedPreferences.setMockInitialValues({'onboarding.complete': true});
    await tester.pumpWidget(const AoGroupeApp());
    await tester.pump(const Duration(milliseconds: 800));
    await tester.pumpAndSettle();

    expect(find.text('أهلاً بك في AO groupe'), findsNothing);
    expect(find.text('كل حلول الكهرباء والطاقة، في مكان واحد'), findsOneWidget);
    expect(
      find.byType(NavigationBar),
      findsOneWidget,
    );
  });

  testWidgets('keeps the design system preview available in settings', (
    tester,
  ) async {
    SharedPreferences.setMockInitialValues({'onboarding.complete': true});
    await tester.pumpWidget(const AoGroupeApp());
    await tester.pump(const Duration(milliseconds: 800));
    await tester.pumpAndSettle();

    await tester.tap(find.text('حسابي'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('الإعدادات'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('معاينة نظام التصميم'));
    await tester.pumpAndSettle();

    expect(find.text('معاينة نظام التصميم'), findsOneWidget);
    expect(find.text('نفد المخزون'), findsOneWidget);
    expect(find.byType(DropdownButton<Locale>), findsOneWidget);
  });
}
