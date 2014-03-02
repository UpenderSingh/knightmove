#include <iostream>
#include <vector>
#include <array>
#include <numeric>
#include <string>
#include <sstream>
#include "kbd.hpp" //generated by make -  see knights_charm.py for how.

//Ideally, we want to use 128-bit integers for storing results, as the value of 
//the output grows exponentially. If you build on 32-bit gcc, this will blow up,
//so comment out the below. Then we fall back to 64bit representation, which is 
//enough for up to 38 or so... 128bit overflows at 80+ path length.
#define use128

struct data {
    //Number of keys on keyboard
    static const size_t size=sizeof(i_to_k); 
#ifdef use128
    typedef unsigned __int128 _i;
#else
    typedef uint64_t _i;
#endif
    /* This is the main datastructure that solves the problem. The insight is 
     * that when we have k moves left, and we have consumed n (n<=2) vowels, we
     * do not actually need the explicit paths of shorter length - we just need
     * to know, for each key, for each possible value of vowels consumed (0,1,2)
     * how many paths of length k-1 are initiated from that key. Thus, level[0] 
     * is the array of path counts assuming we consumed 0 vowels, level[1] is 
     * the same having consumed 1 vowel, and 2 is having consumed 2 vowels.
     */
    typedef std::array<std::array<_i,size>,3> _level;
    
    /*This is to store the individual arrays of path lengths, starting with 2*/
    typedef std::vector<_level> _levels; 
};

#ifdef use128
//not very fast, and does not work for 0. We never output 0, so we do not care.
std::ostream& operator<<(std::ostream& o, unsigned __int128 i) {
    if (!i) return o;
    o << (i/10);
    o << static_cast<char>(i%10+0x30);
    return o;
}
#endif

//Debug function
template <class T> 
void print_level(const T& prefix, const data::_level& level) {
    for(const auto& slevel: level) {
        std::cout << prefix << " [ " ;
        for (auto e: slevel) {
            std::cout << e << ", ";
        }
        std::cout << "]" <<std::endl;
    }
}

/* Compute path counts for all paths of length level, and put into levels. 
 * Assumes that levels[k], 0 <= k < level contains counts of paths of length k.
 * Complexity of 1 step is O(keyboard_size).
 */
void genlevel(data::_i level, data::_levels& levels) {
    data::_level level_cur{}; //We need the initializer here, as we want the
                              //array data to be set to 0.
    if (level==2) {
        /* Base case: we compute all path of 2 keypresses. level_cur[0] counts
           all paths, level_cur[1] counts paths with 1 vowel, and level_cur[2]
           counts paths with 0 vowels. */
        for (size_t from=0;from<data::size;++from) {
            for(auto to: map[from]) {
                if (to==-1) break;
                switch (vowels[from]+vowels[to]) {
                    case 0: level_cur[2][from]++;
                    case 1: level_cur[1][from]++;
                    case 2: level_cur[0][from]++;
                }
            }
        }
    } else {
        /* Recursive case: For a path of length k, basically -  
           1. if we are starting from a vowel, sum up paths of length k-1 that 
              do not need 2 vowels;
           2. if we are starting NOT from a vowel, sum up _all_ paths of length
              k-1. 
         */
        for (size_t from=0;from<data::size;++from) {
            for(auto to: map[from]) {
                if (to==-1) break;
                if (!vowels[from]) {
                    level_cur[0][from]+=levels[level-1][0][to];
                    level_cur[1][from]+=levels[level-1][1][to];
                    level_cur[2][from]+=levels[level-1][2][to];
                } else {
                    level_cur[0][from]+=levels[level-1][1][to];
                    level_cur[1][from]+=levels[level-1][2][to];
                }
            }
        }
    }
    levels.push_back(level_cur);
}

/* Returns the number of valid knight move paths of length 'moves' with at most 
 * 2 vowels in the path. Complexity is O(moves * keyboard_size).
 */
data::_i valid_moves(size_t moves) {
    data::_levels levels(2);
    for (data::_i i=2;i<=moves;++i) {
        genlevel(i,levels);
    }
    std::cout<<std::endl;
    return std::accumulate(levels[moves][0].begin(),levels[moves][0].end(),data::_i{});
}

//stoi missing from cygwin g++ 4.8.2 ?! TODO: kill with fire when bug is fixed.
template <class T>
int stoi(const T& t) {
    std::stringstream ss;
    ss << t;
    int res;
    ss >> res;
    return res;
}

int main(int argc, char** argv) {
    std::cout << valid_moves(argc==1?10:stoi(argv[1])) <<std::endl;
    return 0;
}
