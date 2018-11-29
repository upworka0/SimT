from user_interface.models import PenteOrigineDeDiversitee, CourbeDeDiversitee
import uuid

class Interpolation:
    def __init__(self):
        pass

    def compute_linear_interpolation(self, begin_object, end_object, area_needed):
        """
            Find the slope and the offset for an area outside of the chart by computing
            the linear interpolation of the graph.

            Using the following formula :

            slope of area = recovery(begin slope) + [(delta/difference area begin and end) * (end - begin)]
        """
        total_delta = end_object.courbe_de_diversite_superficie - begin_object.courbe_de_diversite_superficie
        delta_nominator = area_needed - begin_object.courbe_de_diversite_superficie
        delta = delta_nominator / total_delta

        area_slope = self.__compute_slope(delta=delta, begin_m=begin_object.courbe_de_diversite_reprise_m, end_m=end_object.courbe_de_diversite_reprise_m)
        area_offset = self.__compute_offset(delta=delta, begin_b=begin_object.courbe_de_diversite_reprise_b, end_b=end_object.courbe_de_diversite_reprise_b)
        courbe = self.save_courbe_diversite(array={"slope" : area_slope, "offset" : area_offset, "area": area_needed, "code_saison": begin_object.courbe_de_diversite_code_saison})
        courbe_1 = self.compute_linear_interpolation_niveau_diversite(begin_object=begin_object, end_object=end_object, niveau_diversite=1, area_needed=area_needed)
        courbe_200 = self.compute_linear_interpolation_niveau_diversite(begin_object=begin_object, end_object=end_object, niveau_diversite=200, area_needed=area_needed)
        self.save_pente_origine(array=courbe_200, courbe_diversite=courbe)
        self.save_pente_origine(array=courbe_1, courbe_diversite=courbe)
        return courbe

    def compute_linear_interpolation_niveau_diversite(self, begin_object, end_object, niveau_diversite, area_needed):
        """compute_linear_interpolation_niveau_diversite

        :param begin_object:
        :param end_object:
        :param niveau_diversite:
        :param area_needed:
        """
        total_delta = end_object.courbe_de_diversite_superficie - begin_object.courbe_de_diversite_superficie
        delta_nominator = area_needed - begin_object.courbe_de_diversite_superficie
        delta = delta_nominator / total_delta
        # print("Begin Object: {} \nEnd Object: {}\n".format(begin_object, end_object))
        begin_pente = PenteOrigineDeDiversitee.objects.filter(courbe_de_diversite_id=begin_object.courbe_de_diversite_id, pente_origine_diversite_nbr_client=niveau_diversite).get()
        end_pente = PenteOrigineDeDiversitee.objects.filter(courbe_de_diversite_id=end_object.courbe_de_diversite_id, pente_origine_diversite_nbr_client=niveau_diversite).get()
        
        area_slope = self.__compute_slope(delta=delta, begin_m=begin_pente.pente_origine_diversite_m, end_m=end_pente.pente_origine_diversite_m)
        area_offset = self.__compute_offset(delta=delta, begin_b=begin_pente.pente_origine_diversite_b, end_b=end_pente.pente_origine_diversite_b)
        return {"slope" : area_slope, "offset": area_offset, "diversity" : niveau_diversite}
 
    def save_courbe_diversite(self, array):
        """save_courbe_diversite

        :param array:
        """

        courbe = CourbeDeDiversitee.objects.create(
             courbe_de_diversite_id = uuid.uuid1(),
             courbe_de_diversite_reprise_m=array['slope'],
             courbe_de_diversite_reprise_b=array['offset'],
             courbe_de_diversite_superficie=array['area'],
             courbe_de_diversite_code_saison= array['code_saison']
            )
        courbe.save()
        return courbe

    def save_pente_origine(self, array, courbe_diversite):
        """save_pente_origine

        :param array:
        """
        
        pente = PenteOrigineDeDiversitee.objects.create(
            pente_origine_diversite_id= uuid.uuid1(),
            pente_origine_diversite_m=array['slope'],
            pente_origine_diversite_b=array['offset'],
            pente_origine_diversite_nbr_client=array['diversity'],
            courbe_de_diversite_id=courbe_diversite
        )
        pente.save()
        return pente


    def __compute_slope(self, delta, begin_m, end_m):
        """__compute_slope

        :param delta:
        :param begin_object:
        :param end_object:
        """
        difference_end_begin = end_m - begin_m
        product_delta_difference = delta * difference_end_begin
        area_needed_m = begin_m + product_delta_difference
        return area_needed_m

    def __compute_offset(self, delta, begin_b, end_b):
        """__compute_offset

        :param delta:
        :param begin_object:
        :param end_object:
        """
        difference_end_begin = end_b - begin_b
        product_delta_difference = delta * difference_end_begin
        area_needed_b = begin_b + product_delta_difference
        return area_needed_b
