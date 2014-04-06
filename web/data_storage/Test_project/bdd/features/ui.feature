# -- FILE: features/ui.feature
# language: ru
@parallelscenarios
Функционал: Тестируем педант

	Контекст: Подготовка приложения
	 	Допустим открыта главная страница

	@ui @screenshots
	Структура сценария: Пользователь просматривает страницу <page> и ищет текст <text> 
		Если я открою страницу <page>
		То на странице должен быть заголовок <text>
		Но не должно быть текста <bad_text>

	Примеры:
		|page							 |text								   |bad_text|
		|/								 |Here is a project lists:			   |Error	 |
		|/projects/Test_project/edit 	 |Edit project: Test_project 		   |Error	 |
		|/projects/Test_project/bdd/build|Launch BDD Features for Test_project |Error	 |