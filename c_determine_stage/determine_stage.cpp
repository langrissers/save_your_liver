// determine_stage.cpp : 定义 DLL 应用程序的导出函数。
//

#include "stdafx.h"
#include "determine_stage.h"
#include <iostream>
//#include <Windows.h>
#include <iostream>
#include <string>
#include <sstream>
#include <codecvt>
#include <opencv2/opencv.hpp>


//int determine_stage();
std::string pHashValue(cv::Mat& src);
double similarity(cv::Mat, cv::Mat);
int screenshot(std::string fileName, int wmin, int hmin, int wmax, int hmax);
std::wstring utf8_to_utf16(const std::string& text_utf8);
std::string utf16_to_utf8(const std::wstring& text_utf16);

int determine_stage()
{
	int a = 0;
	int result = 0;
	double threshold = 0.9;
	double threshold_strict = 0.99;
	double s1, s2, s3, s4, s351, s352, s353, s451, s452, s453, s551, s552, s553;
	double s_all[30] = { 0 };

	std::string dir_solid_pic("pics\\");


	// std::cout << "C_solid_pic" << dir_solid_pic << std::endl;
	std::string filename = "C:\\screen.bmp";
	screenshot(filename, 0, 0, 1024, 768);
	cv::Mat src_screen = cv::imread(filename);
	cv::Mat im_screen;
	cv::Mat solid_pic;
	cv::Mat tmp_img;
	cv::Rect region;


	// is in main map
	screenshot(filename, 255, 45, 275, 65);
	solid_pic = cv::imread(dir_solid_pic + "0_1_money.bmp");
	s1 = similarity(cv::imread(filename), solid_pic);

	screenshot(filename, 431, 52, 443, 65);
	solid_pic = cv::imread(dir_solid_pic + "0_2_crystal.bmp");
	s2 = similarity(cv::imread(filename), solid_pic);

	screenshot(filename, 614, 46, 625, 59);
	solid_pic = cv::imread(dir_solid_pic + "0_3_stamina.bmp");
	s3 = similarity(cv::imread(filename), solid_pic);

	if (s1 > threshold && s2 > threshold && s3 > threshold)
	{
		result = 100;
	}

	// is_activity
	screenshot(filename, 830, 43, 1000, 66);
	solid_pic = cv::imread(dir_solid_pic + "1_event.bmp");
	s1 = similarity(cv::imread(filename), solid_pic);
	s_all[1] = s1;


	if (s1 > threshold)
		result = 1;

	// is_event_selected
	screenshot(filename, 320, 250, 690, 380);
	solid_pic = cv::imread(dir_solid_pic + "event_35A.bmp");
	s351 = similarity(cv::imread(filename), solid_pic);
	if (s351 > threshold)
	{
		result = 351;
		goto print_and_return;
	}

	screenshot(filename, 320, 250, 690, 380);
	solid_pic = cv::imread(dir_solid_pic + "event_35B.bmp");
	s352 = similarity(cv::imread(filename), solid_pic);
	if (s352 > threshold)
	{
		result = 352;
		goto print_and_return;
	}

	screenshot(filename, 320, 250, 690, 380);
	solid_pic = cv::imread(dir_solid_pic + "event_35C.bmp");
	s353 = similarity(cv::imread(filename), solid_pic);
	if (s353 > threshold)
	{
		result = 353;
		goto print_and_return;
	}

	screenshot(filename, 320, 250, 690, 380);
	solid_pic = cv::imread(dir_solid_pic + "event_45A.bmp");
	s451 = similarity(cv::imread(filename), solid_pic);
	if (s451 > threshold)
	{
		result = 451;
		goto print_and_return;
	}

	screenshot(filename, 320, 250, 690, 380);
	solid_pic = cv::imread(dir_solid_pic + "event_45B.bmp");
	s452 = similarity(cv::imread(filename), solid_pic);
	if (s452 > threshold)
	{
		result = 352;
		goto print_and_return;
	}

	screenshot(filename, 320, 250, 690, 380);
	solid_pic = cv::imread(dir_solid_pic + "event_45C.bmp");
	s453 = similarity(cv::imread(filename), solid_pic);
	if (s453 > threshold)
	{
		result = 453;
		goto print_and_return;
	}

	screenshot(filename, 320, 250, 690, 380);
	solid_pic = cv::imread(dir_solid_pic + "event_55A.bmp");
	s551 = similarity(cv::imread(filename), solid_pic);
	if (s551 > threshold)
	{
		result = 551;
		goto print_and_return;
	}
	screenshot(filename, 320, 250, 690, 380);
	screenshot(filename + "55B", 320, 250, 690, 380);


	solid_pic = cv::imread(dir_solid_pic + "event_55B.bmp");
	s552 = similarity(cv::imread(filename), solid_pic);
	if (s552 > threshold)
	{
		result = 552;
		goto print_and_return;
	}

	screenshot(filename, 320, 250, 690, 380);
	solid_pic = cv::imread(dir_solid_pic + "event_55C.bmp");
	s553 = similarity(cv::imread(filename), solid_pic);
	if (s553 > threshold)
	{
		result = 553;
		goto print_and_return;
	}


	// is battle prepare
	screenshot(filename, 927, 666, 983, 742);
	solid_pic = cv::imread(dir_solid_pic + "2_battle_br.bmp");
	s1 = similarity(cv::imread(filename), solid_pic);
	s_all[2] = s1;
	if (s1 > threshold)
		result = 2;
	std::cout << "dd2" << std::endl;

	// is_hamberger
	screenshot(filename, 440, 272, 580, 393);
	solid_pic = cv::imread(dir_solid_pic + "3_hamberger.bmp");
	s_all[3] = similarity(cv::imread(filename), solid_pic);
	// although the hamberger makes the "team play" gray, it can still match the case "9";
	// goto return immediately
	if (s_all[3] > threshold)
	{
		result = 3;
		goto print_and_return;
	}

	// is_fighting
	screenshot(filename, 25, 45, 140, 75);
	solid_pic = cv::imread(dir_solid_pic + "4_game.bmp");
	s_all[4] = similarity(cv::imread(filename), solid_pic);
	if (s_all[4] > threshold)
		result = 4;

	std::cout << "dd4" << std::endl;

	// is_victory()
	screenshot(filename, 262, 246, 696, 356);
	solid_pic = cv::imread(dir_solid_pic + "5_victory.bmp");
	s_all[5] = similarity(cv::imread(filename), solid_pic);
	if (s_all[5] > threshold)
		result = 5;
	// is_before_auto()
	screenshot(filename, 953, 212, 998, 244);
	solid_pic = cv::imread(dir_solid_pic + "6_auto.bmp");
	s_all[6] = similarity(cv::imread(filename), solid_pic);
	if (s_all[6] > threshold)
		result = 6;

	// is_be_invited()
	screenshot(filename, 117, 222, 147, 256);
	solid_pic = cv::imread(dir_solid_pic + "7_invitation.bmp");
	s1 = similarity(cv::imread(filename), solid_pic);
	screenshot(filename, 114, 281, 156, 317);
	solid_pic = cv::imread(dir_solid_pic + "7_refuse.bmp");
	s2 = similarity(cv::imread(filename), solid_pic);
	s_all[7] = s1 * s2;
	if (s1 > threshold && s2 > threshold)
	{
		int t7_x1 = 140;
		int t7_y1 = 300;
		SetCursorPos(t7_x1, t7_y1);
		mouse_event(MOUSEEVENTF_LEFTDOWN, t7_x1, t7_y1, 0, 0);
		mouse_event(MOUSEEVENTF_LEFTUP, t7_x1, t7_y1, 0, 0);

		std::cout << "refuse invitation" << std::endl;
		// do not return
	}

	// is_in_gym()
	screenshot(filename, 800, 33, 1000, 93);
	// CopyFile(utf8_to_utf16(filename).c_str(), L"C:\\8.bmp", FALSE);
	solid_pic = cv::imread(dir_solid_pic + "91_gym.bmp");
	s_all[8] = similarity(cv::imread(filename), solid_pic);
	if (s_all[8] > threshold)
		result = 8;

	// is_in_exp_training()
	screenshot(filename, 800, 33, 1000, 93);
	solid_pic = cv::imread(dir_solid_pic + "92_exp.bmp");
	s_all[8] = similarity(cv::imread(filename), solid_pic);
	if (s_all[8] > threshold)
		result = 91;

	// is_in_memoria()
	screenshot(filename, 800, 33, 1000, 93);
	solid_pic = cv::imread(dir_solid_pic + "95_memoria.bmp");
	s_all[8] = similarity(cv::imread(filename), solid_pic);
	if (s_all[8] > threshold)
		result = 92;

	//is_in_team():
	screenshot(filename, 800, 33, 1000, 93);
	solid_pic = cv::imread(dir_solid_pic + "90_team.bmp");
	s1 = similarity(cv::imread(filename), solid_pic);
	screenshot(filename, 581, 695, 682, 712);
	solid_pic = cv::imread(dir_solid_pic + "12_finding_team.bmp");
	s2 = similarity(cv::imread(filename), solid_pic);
	s_all[9] = s1;
	s_all[12] = s2;
	if (s1 > threshold && s2 < threshold)
	{

		result = 9;
	}

	else if ((s1 > threshold && s2 > threshold))
	{
		result = 12;
	}

	// is_in_trial()
	screenshot(filename, 800, 33, 1000, 73);
	solid_pic = cv::imread(dir_solid_pic + "93_dragon.bmp");
	s_all[10] = similarity(cv::imread(filename), solid_pic);
	if (s_all[10] > threshold)
		result = 10;
	// is_mysteries()
	screenshot(filename, 902, 30, 1000, 100);
	solid_pic = cv::imread(dir_solid_pic + "11_mysteries.bmp");
	s_all[11] = similarity(cv::imread(filename), solid_pic);
	if (s_all[11] > threshold)
		result = 11;


	// is_more_reward()
	screenshot(filename, 784, 712, 892, 725);
	solid_pic = cv::imread(dir_solid_pic + "15_press_to_continue.bmp");
	if (similarity(cv::imread(filename), solid_pic) > threshold)
		result = 15;
	// is_re_invite()
	screenshot(filename, 400, 300, 600, 500);
	solid_pic = cv::imread(dir_solid_pic + "17_re_invite.bmp");
	if (similarity(cv::imread(filename), solid_pic) > threshold)
		result = 17;
	// is_captain()
	screenshot(filename, 772, 568, 890, 600);
	solid_pic = cv::imread(dir_solid_pic + "18_start_captain.bmp");
	s1 = similarity(cv::imread(filename), solid_pic);
	solid_pic = cv::imread(dir_solid_pic + "20_gray_captain.bmp");
	s2 = similarity(cv::imread(filename), solid_pic);
	if (s1 > threshold || s2 > threshold)
		result = 18;

	// is_store()
	screenshot(filename, 902, 30, 1000, 100);
	solid_pic = cv::imread(dir_solid_pic + "15_press_to_continue.bmp");
	if (similarity(cv::imread(filename), solid_pic) > threshold)
		result = 22;


print_and_return:
	std::cout << "similarity: ";
	for (int isall = 0; isall < 15; isall++)
	{

		if (isall % 5 == 0)
			std::cout << std::endl << "        ";
		std::cout << std::setw(12) << s_all[isall] << " ";

	}
	std::cout << std::endl;
	std::cout << "determine result: " << result << std::endl;
	return result;
}

double similarity(cv::Mat p1, cv::Mat p2)
{
	std::string h1;
	std::string h2;
	h1 = pHashValue(p1);
	h2 = pHashValue(p2);

	int similarity = 0;
	for (int i = 0; i < 64; i++)
		if (h1[i] == h2[i])
			similarity++;
	return similarity / 64.0;
}


//pHash Calculation
std::string pHashValue(cv::Mat & src)
{
	cv::Mat img, dst;
	std::string rst(64, '\0');
	int irst[64];
	double dIdex[64];
	double mean = 0.0;
	int k = 0;
	if (src.channels() == 3)
	{
		cvtColor(src, src, CV_BGR2GRAY);
		img = cv::Mat_<double>(src);
	}
	else
	{
		img = cv::Mat_<double>(src);
	}

	resize(img, img, cv::Size(8, 8));

	dct(img, dst);

	for (int i = 0; i < 8; ++i) {
		for (int j = 0; j < 8; ++j)
		{
			dIdex[k] = dst.at<double>(i, j);
			mean += dst.at<double>(i, j) / 64;
			++k;
		}
	}

	for (int i = 0; i < 64; ++i)
	{
		if (dIdex[i] >= mean)
		{
			rst[i] = '1';
			irst[i] = 1;
		}
		else
		{
			rst[i] = '0';
			irst[i] = 0;
		}
	}
	return rst;
}

std::wstring utf8_to_utf16(const std::string & text_utf8)
{
	return std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>>().from_bytes(text_utf8.c_str());
}

std::string utf16_to_utf8(const std::wstring & text_utf16)
{
	return std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>>().to_bytes(text_utf16.c_str());
}

// Screenshot

int screenshot(std::string fileName, int wmin, int hmin, int wmax, int hmax)
{
	HWND hWnd = 0;
	HDC hdcScreen;
	HDC hdcWindow;
	HDC hdcMemDC = NULL;
	HBITMAP hbmScreen = NULL;
	BITMAP bmpScreen;

	// Retrieve the handle to a display device context for the client 
	// area of the window. 
	hdcScreen = GetDC(NULL);
	hdcWindow = GetDC(hWnd);

	// Create a compatible DC which is used in a BitBlt from the window DC
	hdcMemDC = CreateCompatibleDC(hdcWindow);

	if (!hdcMemDC)
	{
		DeleteObject(hbmScreen);
		DeleteObject(hdcMemDC);
		ReleaseDC(NULL, hdcScreen);
		ReleaseDC(hWnd, hdcWindow);

		return 0;
	}

	hbmScreen = CreateCompatibleBitmap(hdcWindow, wmax - wmin, hmax - hmin);

	if (!hbmScreen)
	{
		DeleteObject(hbmScreen);
		DeleteObject(hdcMemDC);
		ReleaseDC(NULL, hdcScreen);
		ReleaseDC(hWnd, hdcWindow);

		return 0;
	}

	// Select the compatible bitmap into the compatible memory DC.
	SelectObject(hdcMemDC, hbmScreen);

	// Bit block transfer into our compatible memory DC.
	if (!BitBlt(hdcMemDC,
		0, 0,
		wmax - wmin, hmax - hmin,
		hdcWindow,
		wmin, hmin,
		SRCCOPY))
	{
		DeleteObject(hbmScreen);
		DeleteObject(hdcMemDC);
		ReleaseDC(NULL, hdcScreen);
		ReleaseDC(hWnd, hdcWindow);

		return 0;
	}

	// Get the BITMAP from the HBITMAP
	GetObject(hbmScreen, sizeof(BITMAP), &bmpScreen);

	BITMAPFILEHEADER   bmfHeader;
	BITMAPINFOHEADER   bi;

	bi.biSize = sizeof(BITMAPINFOHEADER);
	bi.biWidth = bmpScreen.bmWidth;
	bi.biHeight = bmpScreen.bmHeight;
	bi.biPlanes = 1;
	bi.biBitCount = 32;
	bi.biCompression = BI_RGB;
	bi.biSizeImage = 0;
	bi.biXPelsPerMeter = 0;
	bi.biYPelsPerMeter = 0;
	bi.biClrUsed = 0;
	bi.biClrImportant = 0;

	DWORD dwBmpSize = ((bmpScreen.bmWidth * bi.biBitCount + 31) / 32) * 4 * bmpScreen.bmHeight;

	// Starting with 32-bit Windows, GlobalAlloc and LocalAlloc are implemented as wrapper functions that 
	// call HeapAlloc using a handle to the process's default heap. Therefore, GlobalAlloc and LocalAlloc 
	// have greater overhead than HeapAlloc.
	HANDLE hDIB = GlobalAlloc(GHND, dwBmpSize);
	char* lpbitmap = (char*)GlobalLock(hDIB);

	// Gets the "bits" from the bitmap and copies them into a buffer 
	// which is pointed to by lpbitmap.
	GetDIBits(hdcWindow, hbmScreen, 0,
		(UINT)bmpScreen.bmHeight,
		lpbitmap,
		(BITMAPINFO*)& bi, DIB_RGB_COLORS);

	// A file is created, this is where we will save the screen capture.
	std::wstring wch_name = utf8_to_utf16(fileName);
	HANDLE hFile = CreateFile(wch_name.c_str(),
		GENERIC_WRITE,
		0,
		NULL,
		CREATE_ALWAYS,
		FILE_ATTRIBUTE_NORMAL, NULL);

	// Add the size of the headers to the size of the bitmap to get the total file size
	DWORD dwSizeofDIB = dwBmpSize + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

	//Offset to where the actual bitmap bits start.
	bmfHeader.bfOffBits = (DWORD)sizeof(BITMAPFILEHEADER) + (DWORD)sizeof(BITMAPINFOHEADER);

	//Size of the file
	bmfHeader.bfSize = dwSizeofDIB;

	//bfType must always be BM for Bitmaps
	bmfHeader.bfType = 0x4D42; //BM   

	DWORD dwBytesWritten = 0;
	WriteFile(hFile, (LPSTR)& bmfHeader, sizeof(BITMAPFILEHEADER), &dwBytesWritten, NULL);
	WriteFile(hFile, (LPSTR)& bi, sizeof(BITMAPINFOHEADER), &dwBytesWritten, NULL);
	WriteFile(hFile, (LPSTR)lpbitmap, dwBmpSize, &dwBytesWritten, NULL);

	//Unlock and Free the DIB from the heap
	GlobalUnlock(hDIB);
	GlobalFree(hDIB);

	//Close the handle for the file that was created
	CloseHandle(hFile);

	//Clean up

	DeleteObject(hbmScreen);
	DeleteObject(hdcMemDC);
	ReleaseDC(NULL, hdcScreen);
	ReleaseDC(hWnd, hdcWindow);

	return 0;
}