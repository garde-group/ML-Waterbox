#include <iostream>
#include <fstream>
#include <chrono>
#include <cmath>


int main() { 
    double ** data = new double*[12052];
    int * results = new int[12052];
    std::ifstream file("bf.dat");
    double temp;
    double dx, dy, dz, len;
    const double reff = 0.23328;

    for (int i = 0; i < 12052; i++) {
        data[i] = new double[64];
        for (int j = 0; j < 64; j++) {
            file >> temp;
            data[i][j] = temp;
        }
    }
    std::chrono::high_resolution_clock::time_point start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 12052; i++) {
        for (int j = 3; j < 61; j+=3) {
            dx = std::abs(data[i][0] - data[i][j]);
            dy = std::abs(data[i][1] - data[i][j+1]);
            dz = std::abs(data[i][2] - data[i][j+2]);
            len = sqrt(dx*dx + dy*dy + dz*dz);
            if (len < reff) { 
                results[i] = 0;
                break;
            } else if (j == 60) { 
                results[i] = 1;
            }
        }
    }    
    std::chrono::high_resolution_clock::time_point end = std::chrono::high_resolution_clock::now();

    double total = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
    int zeros = 0;
    int ones = 0; 
    for (int i = 0; i < 12052; i++) {
        if (results[i] == 0) {
            zeros += 1;
        } else if (results[i] == 1) {
            ones += 1;
        } else {
            std::cerr << "ERROR" << std::endl;
        }
    }
    std::cout << "Time: " << total << " Zeros: " << zeros << " Ones: " << ones << std::endl;
    return 0;
}
