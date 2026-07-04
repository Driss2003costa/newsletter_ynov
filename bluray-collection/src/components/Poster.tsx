import Image from "next/image";
import { posterUrl } from "@/lib/image";

type Props = {
  path: string | null | undefined;
  title: string;
  size?: "w185" | "w342" | "w500";
  priority?: boolean;
};

// Affiche l'affiche du film, avec un joli placeholder si aucune image.
export function Poster({ path, title, size = "w500", priority = false }: Props) {
  const url = posterUrl(path, size);

  if (!url) {
    return (
      <div className="flex h-full w-full items-center justify-center bg-gradient-to-br from-panel2 to-panel p-3 text-center">
        <span className="line-clamp-4 text-sm font-medium text-muted">{title}</span>
      </div>
    );
  }

  return (
    <Image
      src={url}
      alt={`Affiche de ${title}`}
      fill
      priority={priority}
      sizes="(max-width: 640px) 45vw, (max-width: 1024px) 30vw, 200px"
      className="object-cover"
    />
  );
}
