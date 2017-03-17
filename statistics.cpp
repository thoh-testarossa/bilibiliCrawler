#include <iostream>
#include <fstream>
#include <string>

#define STATISTICS_SIZE 3000

using namespace std;

typedef struct ymd
{
	int year;
	int month;
	int day;
}ymd;

bool isLegalDate(int year, int month, int day)
{
	int m_12_a[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
	int m_12_b[13] = {0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
	if(year % 4 != 0 || year % 100 == 0 && year % 400 != 0) return (month >= 1) && (month <= 12) && (day <= m_12_a[month]);
	else return (month >= 1) && (month <= 12) && (day <= m_12_b[month]);
}

int calDaysFrom20090101(int year, int month, int day)
{
	int m_12_a[12] = {0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334};
	int m_12_b[12] = {0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335};
	int diff_y = year - 2009;
	int diff_m = month - 1;
	int diff_d = day - 1;
	int ans = 0;
	if(diff_y < 0) return -1;
	ans += diff_y * 365;
	ans += diff_y / 4;
	ans -= (diff_y + 8) / 100;
	ans += (diff_y + 8) / 400;
	if(diff_y % 4 != 3) ans += m_12_a[diff_m];
	else ans += m_12_b[diff_m];
	ans += diff_d;
	return ans;
}

int main()
{
	int statistics[STATISTICS_SIZE];
	ymd outputFormat[STATISTICS_SIZE];
	for(int i = 0; i < STATISTICS_SIZE; i++)
		statistics[i] = 0;
	int year, month, day, hour, minute, second;
	ifstream fin("uptime_1_p.txt");
	ofstream fout("statistics_ymd.txt");
	ofstream fout_2("statistics_hours.txt");
	int hours[24] = {0};
	while(fin >> year >> month >> day >> hour >> minute >> second)
	{	
		if(isLegalDate(year, month, day))
		{
			outputFormat[calDaysFrom20090101(year, month, day)].year = year;
			outputFormat[calDaysFrom20090101(year, month, day)].month = month;
			outputFormat[calDaysFrom20090101(year, month, day)].day = day;
			statistics[calDaysFrom20090101(year, month, day)]++;
			
			hours[hour]++;
		}
	}
	for(int i = 0; i < STATISTICS_SIZE; i++)
	{
		if(statistics[i] != 0)
			fout << outputFormat[i].year << "-" << outputFormat[i].month << "-" << outputFormat[i].day << " " << statistics[i] << "\n";
	}
	for(int i = 0; i < 24; i++)
		fout_2 << hours[i] << " ";
	fout_2 << "\n";
	fin.close();
	fout.close();
	fout_2.close();
	return 0;
}
