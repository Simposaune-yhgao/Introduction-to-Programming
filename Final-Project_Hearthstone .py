#include<stdio.h>
#include"QF100300s14_final_api.c"


int main() {
    struct CARD my_card[30] ;
    struct CARD competitor_card[30] ;
    struct ATTACK attack_log[7] ;
    int attack_times ;

    char competitor[128] ; // name of your competitor
    int offensive ; // 1 means you move first.
    int my_hp ; // 30 initially, you lose when it become 0
    int competitor_hp ;
    int curr_round ;
    int cost ;

    int i , j ,k;
    int card_num ;
    int taunt_id ;
    int chupai[99]={0};

    int self_sel_id[30] = {4,4,5,5,7,7,10,10,13,13,15,15,16,16,29,29,27,27,30,36,36,43,43,50,50,52,59,59,66,70};
    //  1. read game setup
    game_setup( competitor , & offensive ) ;

    //  2. select your card set
        // 2 ways:
        // 1. pre-defined carsets, 1~5
        ////////////////////////////////////////////////////
            //select_cardset ( 2 ) ;
        ////////////////////////////////////////////////////
        // 2. self-select, select -1 and call "self_select" function
            select_cardset ( -1 ) ;
            self_select ( self_sel_id ) ;
        ////////////////////////////////////////////////////

    //  3. game start
      while ( 1 ) {
        get_situation ( &curr_round , &cost , &attack_times , attack_log , my_card , competitor_card , &my_hp , &competitor_hp ) ;
        if ( my_hp == 0 || competitor_hp == 0 ) break ;

        // 算場上有幾張牌
        //////////////////////////////
        // Add your algorithm here: //

        // count cards
        card_num = 0 ;
        for ( i = 0 ; my_card[i].index != -1 ; i ++ ) {
			if ( my_card[i].show_round != -1 && my_card[i].hp_rest > 0 ) {
				card_num ++ ;
			}
        }
        // put card:
      for ( i = 0 ; my_card[i].index != -1 && card_num < 7 ; i ++ ) {
            if ( my_card[i].show_round == -1 && my_card[i].hp_rest > 0 && my_card[i].cost <= cost&&my_card[i].atk>3) {
                put_card( i ) ;
                card_num ++ ;
                cost = cost - my_card[i].cost ;
            }
            else if(my_card[i].show_round == -1 && my_card[i].hp_rest > 0 && my_card[i].cost <= cost&&my_card[i].atk<=3){
                put_card( i ) ;
                card_num ++ ;
                cost = cost - my_card[i].cost ;
            }
        }


        // attack
        for ( i = 0 ; my_card[i].index != -1 ; i ++ ) {
            if ( my_card[i].show_round != -1 && my_card[i].hp_rest > 0 && my_card[i].atk > 0 &&my_card[i].atk<=3) {
                taunt_id = -1 ;

                for ( j = 0 ; j <= 29 ; j ++ ) {
                    if ( competitor_card[j].index != -1 && competitor_card[j].hp_rest > 0 && competitor_card[j].taunt == 1 ) {
                        taunt_id = j ;
                        break ;
                    }
                }

                attack( i , taunt_id ) ;
                if ( taunt_id >= 0 ) {
                    my_card[i].hp_rest = my_card[i].hp_rest - competitor_card[taunt_id].atk ;
                    competitor_card[taunt_id].hp_rest = competitor_card[taunt_id].hp_rest - my_card[i].atk ;
                    break;
                }

        }

          else if ( my_card[i].show_round != -1 && my_card[i].hp_rest > 0 && my_card[i].atk > 0 &&my_card[i].atk>3) {

                taunt_id = -1 ;

                for ( j = 0 ; j <= 29 ; j ++ ) {
                    if ( competitor_card[j].index != -1 && competitor_card[j].hp_rest > 0 && competitor_card[j].taunt == 0&& competitor_card[j].hp_rest==my_card[i].atk) {
                        taunt_id = j ;
                        break ;
                    }
                }
                for ( j = 0 ; j <= 29 ; j ++ ) {
                    if ( competitor_card[j].index != -1 && competitor_card[j].hp_rest > 0 && competitor_card[j].taunt == 1 ) {
                        taunt_id = j ;
                        break ;
                    }
                }



                attack( i , taunt_id ) ;
                if ( taunt_id >= 0 ) {
                    my_card[i].hp_rest = my_card[i].hp_rest - competitor_card[taunt_id].atk ;
                    competitor_card[taunt_id].hp_rest = competitor_card[taunt_id].hp_rest - my_card[i].atk ;
                }
          }
        }//for






        //////////////////////////////
        round_finish () ;
      }

    return 0 ;
}
