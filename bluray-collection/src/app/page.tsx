import { prisma } from "@/lib/prisma";
import { CollectionGrid } from "@/components/CollectionGrid";
import type { BluRayItem } from "@/lib/types";

// La collection change à chaque ajout/suppression : on ne met pas en cache.
export const dynamic = "force-dynamic";

export default async function HomePage() {
  const rows = await prisma.bluRay.findMany({ orderBy: { createdAt: "desc" } });

  const items: BluRayItem[] = rows.map(({ updatedAt, createdAt, ...r }) => ({
    ...r,
    createdAt: createdAt.toISOString(),
  }));

  return <CollectionGrid initialItems={items} />;
}
