#include <fstream>
#include <string>
using namespace std;

void toBlank(string &a)
{
	for(int i = 0; i < a.length(); i++)
	{
		if(!isdigit(a[i]))
			a[i] = ' ';
	}
}

int main()
{
	ifstream fin("test_avid_uptime.txt");
	ofstream fout("test_avid_uptime_1.txt");
	string tmp;
	while(getline(fin, tmp))
	{
		toBlank(tmp);
		fout << tmp << "\n";
	}
	fin.close();
	fout.close();
	return 0;
}
